import argparse
import json
import re
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCAN_REGISTER_PATH = REPO_ROOT / ".agent" / "data" / "forum_scan_register.json"
TOPIC_PATTERN = re.compile(r'<a [^>]*class="topictitle"[^>]*>([^<]+)</a>', re.DOTALL)
ATTR_PATTERN = re.compile(r'(\w+)="([^"]+)"')

FORUM_ALLOWLIST = {
    "bekanntmachungen": {
        "forum_id": 6,
        "label": "Bekanntmachungen",
        "docs_dir": REPO_ROOT / "docs" / "Quellen" / "Forum" / "Bekanntmachungen",
        "default_pages": 3,
        "human_review_required": False,
        "status": "archiviert",
    },
    "news": {
        "forum_id": 1,
        "label": "Newsticker",
        "docs_dir": REPO_ROOT / "docs" / "Quellen" / "Forum" / "Newsticker",
        "default_pages": 3,
        "human_review_required": False,
        "status": "archiviert",
    },
    "geschichten": {
        "forum_id": 27,
        "label": "Geschichten aus dem Spiel",
        "docs_dir": REPO_ROOT / "docs" / "Quellen" / "Forum" / "Geschichten_aus_dem_Spiel",
        "default_pages": 5,
        "human_review_required": False,
        "status": "archiviert",
    },
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_register() -> dict:
    if not SCAN_REGISTER_PATH.exists():
        return {"version": 1, "boards": {}, "entries": []}
    try:
        return json.loads(SCAN_REGISTER_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"version": 1, "boards": {}, "entries": []}


def save_register(payload: dict) -> None:
    SCAN_REGISTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCAN_REGISTER_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text[:80] or "forum_eintrag"


def extract_iso_date(raw_date: str) -> str | None:
    match = re.search(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", raw_date)
    if not match:
        return None
    day, month, year = match.groups()
    return f"{year}-{int(month):02d}-{int(day):02d}"


def scan_forum(board_key: str, max_pages: int) -> list[dict]:
    cfg = FORUM_ALLOWLIST[board_key]
    forum_id = cfg["forum_id"]
    base_url = f"http://schnellerwind.mind.de/Foren/phpBB3/viewforum.php?f={forum_id}"
    topics: list[dict] = []

    for page in range(max_pages):
        start = page * 40
        url = f"{base_url}&start={start}"
        print(f"Scanning {board_key} page {page + 1} (start={start})...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as response:
                html = response.read().decode("utf-8", "ignore")
                for match in TOPIC_PATTERN.finditer(html):
                    title = match.group(1).strip()
                    attrs = dict(ATTR_PATTERN.findall(match.group(0)))
                    href = attrs.get("href", "")
                    raw_date = attrs.get("title", "").replace("Verfasst: ", "")
                    topic_id_match = re.search(r"t=(\d+)", href)
                    topic_id = topic_id_match.group(1) if topic_id_match else "unknown"
                    topics.append(
                        {
                            "topic_id": topic_id,
                            "title": title,
                            "raw_date": raw_date,
                            "date": extract_iso_date(raw_date),
                            "url": f"http://schnellerwind.mind.de/Foren/phpBB3/viewtopic.php?f={forum_id}&t={topic_id}",
                            "board": board_key,
                            "forum_id": forum_id,
                        }
                    )
            time.sleep(0.5)
        except Exception as exc:
            print(f"Error on page {page}: {exc}")
            break
    return topics


def existing_topic_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    for path in root.rglob("*.md"):
        raw = path.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"^topic_id:\s*(\d+)\s*$", raw, re.MULTILINE)
        if match:
            ids.add(match.group(1))
    return ids


def write_raw_metadata(topic: dict, cfg: dict) -> str | None:
    if topic["topic_id"] == "unknown":
        return None
    docs_dir = cfg["docs_dir"]
    docs_dir.mkdir(parents=True, exist_ok=True)
    date_prefix = topic["date"] or "undated"
    filename = f"{date_prefix}_{slugify(topic['title'])}.md"
    target = docs_dir / filename
    if target.exists():
        return str(target.relative_to(REPO_ROOT))

    human_review_required = "true" if cfg["human_review_required"] else "false"
    body = "\n".join(
        [
            "---",
            f"source: {topic['url']}",
            f"title: {topic['title']}",
            f"date: {topic['date'] or ''}",
            "type: Forum Entry",
            "epistemic: \"#forum\"",
            f"status: {cfg['status']}",
            f"forum: {cfg['label']}",
            f"forum_id: {topic['forum_id']}",
            f"topic_id: {topic['topic_id']}",
            f"human_review_required: {human_review_required}",
            "---",
            "",
            f"# {topic['title']}",
            "",
            "_Metadaten-Archiv aus der Forenuebersicht. Detailinhalt kann bei Bedarf durch Amtspruefung nachgezogen werden._",
            "",
            f"- Forum: **{cfg['label']}**",
            f"- Link: {topic['url']}",
            f"- Topic-ID: `{topic['topic_id']}`",
            f"- Letzte Sichtung: `{now_iso()}`",
            "",
        ]
    )
    target.write_text(body + "\n", encoding="utf-8")
    return str(target.relative_to(REPO_ROOT))


def update_register(board_key: str, pages: int, topics: list[dict], known_topic_ids: set[str], cfg: dict) -> list[dict]:
    payload = load_register()
    entries = payload.setdefault("entries", [])
    boards = payload.setdefault("boards", {})
    results: list[dict] = []

    for topic in topics:
        topic_id = topic["topic_id"]
        decision = "duplicate" if topic_id in known_topic_ids else "new"
        created_ref = None
        if decision == "new":
            created_ref = write_raw_metadata(topic, cfg)
            if created_ref:
                decision = "archived_raw"
        result_entry = {
            "board": board_key,
            "pages_scanned": pages,
            "scanned_at": now_iso(),
            "topic_id": topic_id,
            "title": topic["title"],
            "decision": decision,
            "source_ref": created_ref,
            "dispatch_ref": None,
            "historian_comment": None,
        }
        for idx, existing in enumerate(entries):
            if existing.get("board") == board_key and existing.get("topic_id") == topic_id:
                entries[idx] = result_entry
                break
        else:
            entries.append(result_entry)
        results.append(result_entry)

    boards[board_key] = {
        "forum_id": cfg["forum_id"],
        "label": cfg["label"],
        "last_scanned_at": now_iso(),
        "last_page_scanned": pages,
        "last_seen_topic_id": topics[0]["topic_id"] if topics else None,
    }
    save_register(payload)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Siebenwind Forum Scanner")
    parser.add_argument("--forum-key", choices=sorted(FORUM_ALLOWLIST.keys()), default="bekanntmachungen")
    parser.add_argument("--forum_id", type=int, help="Legacy override for forum ID")
    parser.add_argument("--pages", type=int, help="Number of pages to scan")
    args = parser.parse_args()

    board_key = args.forum_key
    if args.forum_id is not None:
        for key, cfg in FORUM_ALLOWLIST.items():
            if cfg["forum_id"] == args.forum_id:
                board_key = key
                break
    cfg = FORUM_ALLOWLIST[board_key]
    pages = args.pages if args.pages is not None else cfg["default_pages"]

    topics = scan_forum(board_key, max_pages=pages)
    known_topic_ids = existing_topic_ids(REPO_ROOT / "docs" / "Quellen" / "Forum")
    results = update_register(board_key, pages, topics, known_topic_ids, cfg)

    print(f"Done. {board_key}: {len(topics)} Themen gesichtet, {len(results)} Registereintraege aktualisiert.")
    for entry in results[:10]:
        print(f"- {entry['topic_id']} | {entry['decision']} | {entry['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
