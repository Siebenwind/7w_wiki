import argparse
import html as html_lib
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCAN_REGISTER_PATH = REPO_ROOT / ".agent" / "data" / "forum_scan_register.json"
FORUM_BASE_URL = "http://schnellerwind.mind.de/Foren/phpBB3"
TOPIC_PATTERN = re.compile(r'<a [^>]*class="topictitle"[^>]*>([^<]+)</a>', re.DOTALL)
ATTR_PATTERN = re.compile(r'(\w+)="([^"]+)"')

FORUM_ALLOWLIST = {
    "bekanntmachungen": {
        "forum_id": 6,
        "label": "Bekanntmachungen",
        "docs_dir": REPO_ROOT / "docs" / "Quellen" / "Forum" / "Bekanntmachungen",
        "raw_html_dir": REPO_ROOT / "docs" / "Quellen" / "_ARCHIV_ORIGINAL" / "Forum" / "Bekanntmachungen",
        "default_pages": 3,
        "human_escalation_default": False,
        "status": "archiviert",
    },
    "news": {
        "forum_id": 1,
        "label": "Newsticker",
        "docs_dir": REPO_ROOT / "docs" / "Quellen" / "Forum" / "Newsticker",
        "raw_html_dir": REPO_ROOT / "docs" / "Quellen" / "_ARCHIV_ORIGINAL" / "Forum" / "Newsticker",
        "default_pages": 3,
        "human_escalation_default": False,
        "status": "archiviert",
    },
    "geschichten": {
        "forum_id": 27,
        "label": "Geschichten aus dem Spiel",
        "docs_dir": REPO_ROOT / "docs" / "Quellen" / "Forum" / "Geschichten_aus_dem_Spiel",
        "raw_html_dir": REPO_ROOT / "docs" / "Quellen" / "_ARCHIV_ORIGINAL" / "Forum" / "Geschichten_aus_dem_Spiel",
        "default_pages": 5,
        "human_escalation_default": False,
        "status": "archiviert",
    },
}


class ForumTextExtractor(HTMLParser):
    BLOCK_TAGS = {"blockquote", "div", "li", "p", "table", "td", "th", "tr", "ul", "ol"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag == "br" or tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.skip_depth:
            self.skip_depth -= 1
            return
        if not self.skip_depth and tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        raw = "".join(self.parts).replace("\xa0", " ")
        raw = re.sub(r"[ \t\r\f\v]+", " ", raw)
        raw = re.sub(r" *\n *", "\n", raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return raw.strip()


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
    payload.setdefault("version", 1)
    for entry in payload.setdefault("entries", []):
        if "content_status" not in entry and entry.get("source_ref"):
            entry["content_status"] = "metadata_only"
    SCAN_REGISTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCAN_REGISTER_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text[:80] or "forum_eintrag"


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def extract_iso_date(raw_date: str) -> str | None:
    match = re.search(r"(\d{1,2})\.(\d{1,2})\.(\d{2,4})", raw_date or "")
    if not match:
        return None
    day, month, year_text = match.groups()
    year = int(year_text)
    if year < 100:
        year = 2000 + year if year < 70 else 1900 + year
    return f"{year:04d}-{int(month):02d}-{int(day):02d}"


def topic_url(forum_id: int, topic_id: str, start: int | None = None) -> str:
    url = f"{FORUM_BASE_URL}/viewtopic.php?f={forum_id}&t={topic_id}"
    if start:
        url += f"&start={start}"
    return url


def normalize_forum_url(raw_url: str) -> str:
    raw_url = html_lib.unescape(raw_url)
    absolute = urllib.parse.urljoin(f"{FORUM_BASE_URL}/", raw_url)
    parsed = urllib.parse.urlsplit(absolute)
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    query = [(key, value) for key, value in query if key.lower() != "sid"]
    clean_query = urllib.parse.urlencode(query)
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, clean_query, parsed.fragment))


def strip_session_ids_from_html(raw_html: str) -> str:
    cleaned = re.sub(r"([?&])sid=[A-Za-z0-9]+(&amp;|&)", r"\1", raw_html)
    cleaned = re.sub(r"(&amp;|&)sid=[A-Za-z0-9]+", "", cleaned)
    cleaned = re.sub(r"\?sid=[A-Za-z0-9]+", "", cleaned)
    cleaned = re.sub(r"\?(&amp;|&)", "?", cleaned)
    cleaned = re.sub(r"\?([\"'#])", r"\1", cleaned)
    return cleaned


def fetch_url(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        return response.read().decode("utf-8", "ignore")


def html_text(fragment: str) -> str:
    parser = ForumTextExtractor()
    parser.feed(fragment)
    return parser.text()


def scan_forum(board_key: str, max_pages: int, verbose: bool = True) -> list[dict]:
    cfg = FORUM_ALLOWLIST[board_key]
    forum_id = cfg["forum_id"]
    base_url = f"{FORUM_BASE_URL}/viewforum.php?f={forum_id}"
    topics: list[dict] = []

    for page in range(max_pages):
        start = page * 40
        url = f"{base_url}&start={start}"
        if verbose:
            print(f"Scanning {board_key} page {page + 1} (start={start})...")
        try:
            html = fetch_url(url)
            for match in TOPIC_PATTERN.finditer(html):
                title = html_text(match.group(1)).strip()
                attrs = dict(ATTR_PATTERN.findall(match.group(0)))
                href = attrs.get("href", "")
                raw_date = attrs.get("title", "").replace("Verfasst: ", "")
                topic_id_match = re.search(r"t=(\d+)", html_lib.unescape(href))
                topic_id = topic_id_match.group(1) if topic_id_match else "unknown"
                topics.append(
                    {
                        "topic_id": topic_id,
                        "title": title,
                        "raw_date": raw_date,
                        "date": extract_iso_date(raw_date),
                        "url": topic_url(forum_id, topic_id),
                        "board": board_key,
                        "forum_id": forum_id,
                    }
                )
            time.sleep(0.5)
        except Exception as exc:
            if verbose:
                print(f"Error on page {page}: {exc}")
            break
    return topics


def existing_topic_refs(root: Path) -> dict[str, str]:
    refs: dict[str, str] = {}
    if not root.exists():
        return refs
    for path in root.rglob("*.md"):
        raw = path.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"^topic_id:\s*(\d+)\s*$", raw, re.MULTILINE)
        if match:
            refs[match.group(1)] = str(path.relative_to(REPO_ROOT))
    return refs


def read_frontmatter_value(path: Path, key: str) -> str | None:
    if not path.exists():
        return None
    raw = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", raw, re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value.strip('"')
    return value


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

    human_escalation_required = "false"
    body = "\n".join(
        [
            "---",
            f"source: {yaml_string(topic['url'])}",
            f"title: {yaml_string(topic['title'])}",
            f"date: {topic['date'] or ''}",
            "type: Forum Entry",
            "epistemic: \"#forum\"",
            f"status: {cfg['status']}",
            f"forum: {yaml_string(cfg['label'])}",
            f"forum_id: {topic['forum_id']}",
            f"topic_id: {topic['topic_id']}",
            "content_status: metadata_only",
            "review_status: archive_only",
            "review_owner: Scout",
            f"human_escalation_required: {human_escalation_required}",
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


def find_register_entry(entries: list[dict], board_key: str, topic_id: str) -> tuple[int | None, dict | None]:
    for idx, entry in enumerate(entries):
        if entry.get("board") == board_key and str(entry.get("topic_id")) == str(topic_id):
            return idx, entry
    return None, None


def update_register(board_key: str, pages: int, topics: list[dict], known_topic_refs: dict[str, str], cfg: dict) -> list[dict]:
    payload = load_register()
    entries = payload.setdefault("entries", [])
    boards = payload.setdefault("boards", {})
    results: list[dict] = []

    for topic in topics:
        topic_id = topic["topic_id"]
        idx, existing = find_register_entry(entries, board_key, topic_id)
        existing = existing or {}
        existing_ref = existing.get("source_ref")
        known_ref = known_topic_refs.get(topic_id)
        decision = "duplicate" if existing_ref or known_ref else "new"
        created_ref = existing_ref or known_ref
        if decision == "new":
            created_ref = write_raw_metadata(topic, cfg)
            if created_ref:
                decision = "archived_raw"

        result_entry = dict(existing)
        result_entry.update(
            {
                "board": board_key,
                "pages_scanned": pages,
                "scanned_at": now_iso(),
                "topic_id": topic_id,
                "title": topic["title"],
                "decision": decision,
                "source_ref": created_ref,
                "dispatch_ref": existing.get("dispatch_ref"),
                "historian_comment": existing.get("historian_comment"),
            }
        )
        if "content_status" not in result_entry and created_ref:
            result_entry["content_status"] = "metadata_only"
        if idx is None:
            entries.append(result_entry)
        else:
            entries[idx] = result_entry
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


def extract_element_html(fragment: str, tag: str, class_name: str | None = None) -> str | None:
    attr_match = r"[^>]*"
    if class_name:
        attr_match = rf'(?=[^>]*class=["\'][^"\']*\b{re.escape(class_name)}\b[^"\']*["\'])[^>]*'
    start_match = re.search(rf"<{tag}\s+{attr_match}>", fragment, re.IGNORECASE | re.DOTALL)
    if not start_match:
        return None

    depth = 1
    pos = start_match.end()
    tag_re = re.compile(rf"<(/?){tag}\b[^>]*>", re.IGNORECASE | re.DOTALL)
    for match in tag_re.finditer(fragment, pos):
        raw_tag = match.group(0)
        closing = bool(match.group(1))
        self_closing = raw_tag.rstrip().endswith("/>")
        if closing:
            depth -= 1
            if depth == 0:
                return fragment[start_match.end() : match.start()]
        elif not self_closing:
            depth += 1
    return fragment[start_match.end() :]


def extract_topic_title(html: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if match:
        title = html_text(match.group(1))
        title = re.sub(r"^Siebenwind Foren\s+.\s+Thema anzeigen\s+-\s*", "", title).strip()
        if title:
            return title
    h2_match = re.search(r"<h2[^>]*>(.*?)</h2>", html, re.IGNORECASE | re.DOTALL)
    if h2_match:
        return html_text(h2_match.group(1))
    return "Forum Topic"


def extract_page_count(html: str) -> int:
    text = html_text(html)
    matches = re.findall(r"Seite\s+\d+\s+von\s+(\d+)", text)
    if not matches:
        return 1
    return max(int(value) for value in matches)


def discover_topic_starts(html: str, topic_id: str, max_topic_pages: int) -> list[int]:
    starts = {0}
    for href in re.findall(r'href=["\']([^"\']*viewtopic\.php[^"\']*)["\']', html, re.IGNORECASE):
        clean_href = normalize_forum_url(href)
        parsed = urllib.parse.urlsplit(clean_href)
        params = urllib.parse.parse_qs(parsed.query)
        if params.get("t", [None])[0] == str(topic_id) and "start" in params:
            try:
                starts.add(int(params["start"][0]))
            except (TypeError, ValueError):
                pass

    page_count = extract_page_count(html)
    if page_count > len(starts):
        for page_idx in range(page_count):
            starts.add(page_idx * 15)

    return sorted(starts)[: max(1, max_topic_pages)]


def parse_posts_from_page(html: str) -> list[dict]:
    anchors = list(re.finditer(r'<a\s+name=["\']p(\d+)["\']\s*>\s*</a>', html, re.IGNORECASE))
    posts: list[dict] = []
    for idx, anchor in enumerate(anchors):
        post_id = anchor.group(1)
        end = anchors[idx + 1].start() if idx + 1 < len(anchors) else len(html)
        block = html[anchor.start() : end]

        author = ""
        author_match = re.search(r'<b\s+class=["\']postauthor["\'][^>]*>(.*?)</b>', block, re.IGNORECASE | re.DOTALL)
        if author_match:
            author = html_text(author_match.group(1))

        subject = ""
        subject_match = re.search(r"Betreff des Beitrags:\s*</b>\s*(.*?)</div>", block, re.IGNORECASE | re.DOTALL)
        if subject_match:
            subject = html_text(subject_match.group(1))

        posted_raw = ""
        posted_match = re.search(r"<b>\s*Verfasst:\s*</b>\s*([^<]+)", block, re.IGNORECASE | re.DOTALL)
        if posted_match:
            posted_raw = html_text(posted_match.group(1))

        body_html = extract_element_html(block, "div", "postbody")
        body = html_text(body_html or "")
        body = re.sub(r"\n{3,}", "\n\n", body).strip()

        posts.append(
            {
                "post_id": post_id,
                "author": author,
                "subject": subject,
                "posted_raw": posted_raw,
                "posted_date": extract_iso_date(posted_raw),
                "body": body,
            }
        )
    return posts


def fetch_topic_pages(board_key: str, topic_id: str, max_topic_pages: int) -> list[dict]:
    cfg = FORUM_ALLOWLIST[board_key]
    forum_id = cfg["forum_id"]
    first_url = topic_url(forum_id, topic_id)
    first_html = fetch_url(first_url)
    starts = discover_topic_starts(first_html, topic_id, max_topic_pages)
    pages: list[dict] = [{"page_number": 1, "start": 0, "url": first_url, "html": first_html}]

    for page_number, start in enumerate([value for value in starts if value != 0], start=2):
        url = topic_url(forum_id, topic_id, start=start)
        pages.append({"page_number": page_number, "start": start, "url": url, "html": fetch_url(url)})
        time.sleep(0.5)

    return pages


def parse_topic_pages(pages: list[dict]) -> dict:
    title = extract_topic_title(pages[0]["html"]) if pages else "Forum Topic"
    posts: list[dict] = []
    for page in pages:
        posts.extend(parse_posts_from_page(page["html"]))
    first_post_date = next((post.get("posted_date") for post in posts if post.get("posted_date")), None)
    return {
        "title": title,
        "date": first_post_date,
        "posts": posts,
        "post_count": len(posts),
        "topic_pages_archived": len(pages),
    }


def source_file_has_fulltext(source_ref: str | None) -> bool:
    if not source_ref:
        return False
    path = REPO_ROOT / source_ref
    if not path.exists():
        return False
    raw = path.read_text(encoding="utf-8", errors="ignore")
    return bool(re.search(r"^content_status:\s*fulltext_archived\s*$", raw, re.MULTILINE))


def raw_refs_with_session_ids(raw_refs: list[str]) -> list[str]:
    dirty: list[str] = []
    for ref in raw_refs:
        path = REPO_ROOT / ref
        if not path.exists():
            continue
        raw = path.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"[?&](?:amp;)?sid=", raw):
            dirty.append(ref)
    return dirty


def sanitize_existing_raw_refs(raw_refs: list[str]) -> None:
    for ref in raw_refs:
        path = REPO_ROOT / ref
        if not path.exists():
            continue
        raw = path.read_text(encoding="utf-8", errors="ignore")
        cleaned = strip_session_ids_from_html(raw)
        if cleaned != raw:
            path.write_text(cleaned, encoding="utf-8")


def planned_source_ref(topic: dict, cfg: dict, parsed: dict | None = None, existing_ref: str | None = None) -> str:
    if existing_ref:
        return existing_ref
    title = (parsed or {}).get("title") or topic.get("title") or f"topic_{topic['topic_id']}"
    date = (parsed or {}).get("date") or topic.get("date") or "undated"
    target = cfg["docs_dir"] / f"{date}_{slugify(title)}.md"
    return str(target.relative_to(REPO_ROOT))


def raw_html_refs(topic_id: str, page_count: int, cfg: dict) -> list[str]:
    refs: list[str] = []
    for idx in range(page_count):
        filename = f"{topic_id}.html" if idx == 0 else f"{topic_id}_p{idx + 1}.html"
        refs.append(str((cfg["raw_html_dir"] / filename).relative_to(REPO_ROOT)))
    return refs


def write_topic_markdown(topic: dict, cfg: dict, parsed: dict, source_ref: str, raw_refs: list[str]) -> None:
    target = REPO_ROOT / source_ref
    target.parent.mkdir(parents=True, exist_ok=True)
    source_url = topic_url(cfg["forum_id"], topic["topic_id"])
    date = parsed.get("date") or topic.get("date") or ""
    title = parsed.get("title") or topic.get("title") or f"Topic {topic['topic_id']}"
    human_escalation_required = "false"

    lines: list[str] = [
        "---",
        f"source: {yaml_string(source_url)}",
        f"source_url: {yaml_string(source_url)}",
        f"title: {yaml_string(title)}",
        f"date: {date}",
        "type: Forum Entry",
        "epistemic: \"#forum\"",
        f"status: {cfg['status']}",
        f"forum: {yaml_string(cfg['label'])}",
        f"forum_id: {cfg['forum_id']}",
        f"topic_id: {topic['topic_id']}",
        "content_status: fulltext_archived",
        "review_status: triage_ready",
        "review_owner: Scout",
        f"human_escalation_required: {human_escalation_required}",
        f"archived_at: {yaml_string(now_iso())}",
        f"post_count: {parsed['post_count']}",
        f"topic_pages_archived: {parsed['topic_pages_archived']}",
        "raw_html_refs:",
    ]
    lines.extend([f"  - {yaml_string(ref)}" for ref in raw_refs])
    lines.extend(
        [
            "---",
            "",
            f"# {title}",
            "",
            "_Archivierter Volltext aus dem Siebenwind-Forum. Diese Quelle ist ein Forum-/Perspektivtext und nicht automatisch kanonisiert._",
            "",
            f"- Forum: **{cfg['label']}**",
            f"- Link: {source_url}",
            f"- Topic-ID: `{topic['topic_id']}`",
            f"- Archiviert am: `{now_iso()}`",
            "",
        ]
    )

    for idx, post in enumerate(parsed["posts"], start=1):
        subject = post.get("subject") or f"Beitrag {idx}"
        lines.extend(
            [
                f"## Beitrag {idx}: {subject}",
                "",
                f"- Autor: `{post.get('author') or 'unbekannt'}`",
                f"- Verfasst: `{post.get('posted_raw') or 'unbekannt'}`",
                f"- Post-ID: `p{post.get('post_id')}`",
                "",
                post.get("body") or "[LEERER_BEITRAG]",
                "",
            ]
        )

    target.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def update_fulltext_register(
    board_key: str,
    topic: dict,
    parsed: dict | None,
    source_ref: str | None,
    raw_refs: list[str],
    status: str,
    error: str | None = None,
) -> None:
    payload = load_register()
    entries = payload.setdefault("entries", [])
    idx, existing = find_register_entry(entries, board_key, topic["topic_id"])
    entry = dict(existing or {})
    entry.update(
        {
            "board": board_key,
            "topic_id": topic["topic_id"],
            "title": (parsed or {}).get("title") or topic.get("title") or entry.get("title"),
            "decision": status,
            "source_ref": source_ref or entry.get("source_ref"),
            "content_status": "fulltext_archived" if status == "archived_fulltext" else entry.get("content_status", "metadata_only"),
            "fulltext_ref": source_ref or entry.get("fulltext_ref"),
            "raw_html_refs": raw_refs or entry.get("raw_html_refs", []),
            "post_count": (parsed or {}).get("post_count", entry.get("post_count")),
            "fulltext_archived_at": now_iso() if status == "archived_fulltext" else entry.get("fulltext_archived_at"),
            "last_error": error,
            "dispatch_ref": entry.get("dispatch_ref"),
            "historian_comment": entry.get("historian_comment"),
        }
    )
    if idx is None:
        entries.append(entry)
    else:
        entries[idx] = entry
    save_register(payload)


def topic_from_register_or_id(board_key: str, topic_id: str) -> dict:
    cfg = FORUM_ALLOWLIST[board_key]
    payload = load_register()
    _, entry = find_register_entry(payload.get("entries", []), board_key, topic_id)
    entry = entry or {}
    source_ref = entry.get("source_ref")
    title = entry.get("title") or f"Topic {topic_id}"
    date = None
    if source_ref:
        path = REPO_ROOT / source_ref
        title = read_frontmatter_value(path, "title") or title
        date = read_frontmatter_value(path, "date")
    return {
        "topic_id": topic_id,
        "title": title,
        "raw_date": "",
        "date": date,
        "url": topic_url(cfg["forum_id"], topic_id),
        "board": board_key,
        "forum_id": cfg["forum_id"],
        "source_ref": source_ref,
    }


def archive_topic_fulltext(board_key: str, topic: dict, dry_run: bool, max_topic_pages: int) -> dict:
    cfg = FORUM_ALLOWLIST[board_key]
    known_refs = existing_topic_refs(REPO_ROOT / "docs" / "Quellen" / "Forum")
    payload = load_register()
    _, entry = find_register_entry(payload.get("entries", []), board_key, topic["topic_id"])
    existing_ref = topic.get("source_ref") or (entry or {}).get("source_ref") or known_refs.get(topic["topic_id"])

    if source_file_has_fulltext(existing_ref):
        raw_refs = (entry or {}).get("raw_html_refs", [])
        dirty_raw_refs = raw_refs_with_session_ids(raw_refs)
        if dirty_raw_refs:
            if not dry_run:
                sanitize_existing_raw_refs(dirty_raw_refs)
            return {
                "topic_id": topic["topic_id"],
                "title": topic.get("title") or (entry or {}).get("title"),
                "status": "would_sanitize_raw_html" if dry_run else "sanitized_raw_html",
                "source_ref": existing_ref,
                "raw_html_refs": raw_refs,
                "sanitized_raw_refs": dirty_raw_refs,
                "post_count": (entry or {}).get("post_count"),
            }
        return {
            "topic_id": topic["topic_id"],
            "title": topic.get("title") or (entry or {}).get("title"),
            "status": "already_fulltext",
            "source_ref": existing_ref,
            "raw_html_refs": raw_refs,
            "post_count": (entry or {}).get("post_count"),
        }

    try:
        pages = fetch_topic_pages(board_key, topic["topic_id"], max_topic_pages=max_topic_pages)
        parsed = parse_topic_pages(pages)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        if not dry_run:
            update_fulltext_register(board_key, topic, None, existing_ref, [], "fulltext_error", error=error)
        return {
            "topic_id": topic["topic_id"],
            "title": topic.get("title"),
            "status": "fulltext_error",
            "source_ref": existing_ref,
            "error": error,
        }

    source_ref = planned_source_ref(topic, cfg, parsed=parsed, existing_ref=existing_ref)
    raw_refs = raw_html_refs(topic["topic_id"], len(pages), cfg)
    result = {
        "topic_id": topic["topic_id"],
        "title": parsed["title"],
        "status": "would_archive_fulltext" if dry_run else "archived_fulltext",
        "source_ref": source_ref,
        "raw_html_refs": raw_refs,
        "post_count": parsed["post_count"],
        "topic_pages_archived": parsed["topic_pages_archived"],
    }

    if parsed["post_count"] == 0:
        result["status"] = "no_posts"
        if not dry_run:
            update_fulltext_register(board_key, topic, parsed, source_ref, raw_refs, "no_posts", error="No post bodies parsed")
        return result

    if dry_run:
        return result

    cfg["raw_html_dir"].mkdir(parents=True, exist_ok=True)
    for page, raw_ref in zip(pages, raw_refs, strict=False):
        (REPO_ROOT / raw_ref).write_text(strip_session_ids_from_html(page["html"]), encoding="utf-8")

    write_topic_markdown(topic, cfg, parsed, source_ref, raw_refs)
    update_fulltext_register(board_key, topic, parsed, source_ref, raw_refs, "archived_fulltext")
    return result


def summarize_results(results: list[dict]) -> dict:
    summary: dict[str, int] = {}
    for result in results:
        status = result.get("status") or result.get("decision") or "unknown"
        summary[status] = summary.get(status, 0) + 1
    return summary


def print_json(payload: dict) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description="Siebenwind Forum Scanner")
    parser.add_argument("--forum-key", choices=sorted(FORUM_ALLOWLIST.keys()), default="bekanntmachungen")
    parser.add_argument("--forum_id", type=int, help="Legacy override for forum ID")
    parser.add_argument("--pages", type=int, help="Number of pages to scan")
    parser.add_argument("--archive-fulltext", action="store_true", help="Archive full topic texts for selected or discovered topics")
    parser.add_argument("--topic-id", help="Archive one specific topic ID")
    parser.add_argument("--limit", type=int, help="Limit fulltext archive attempts")
    parser.add_argument("--dry-run", action="store_true", help="Preview writes without changing files")
    parser.add_argument("--max-topic-pages", type=int, default=20, help="Maximum topic pages to fetch")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    board_key = args.forum_key
    if args.forum_id is not None:
        for key, cfg in FORUM_ALLOWLIST.items():
            if cfg["forum_id"] == args.forum_id:
                board_key = key
                break
    cfg = FORUM_ALLOWLIST[board_key]
    pages = args.pages if args.pages is not None else cfg["default_pages"]

    if args.topic_id:
        topics = [topic_from_register_or_id(board_key, args.topic_id)]
        scan_results: list[dict] = []
    else:
        topics = scan_forum(board_key, max_pages=pages, verbose=not args.json)
        known_topic_refs = existing_topic_refs(REPO_ROOT / "docs" / "Quellen" / "Forum")
        scan_results = [] if args.dry_run else update_register(board_key, pages, topics, known_topic_refs, cfg)

    archive_results: list[dict] = []
    if args.archive_fulltext:
        archive_topics = topics
        if args.limit is not None:
            archive_topics = archive_topics[: max(0, args.limit)]
        for topic in archive_topics:
            if topic.get("topic_id") == "unknown":
                archive_results.append({"topic_id": "unknown", "status": "skipped_unknown_topic", "title": topic.get("title")})
                continue
            archive_results.append(
                archive_topic_fulltext(
                    board_key,
                    topic,
                    dry_run=args.dry_run,
                    max_topic_pages=max(1, args.max_topic_pages),
                )
            )
    else:
        archive_results = scan_results

    if not args.dry_run:
        save_register(load_register())

    payload = {
        "status": "ok" if not any(r.get("status") in {"fulltext_error", "no_posts"} for r in archive_results) else "warn",
        "mode": "fulltext_archive" if args.archive_fulltext else "metadata_scan",
        "board": board_key,
        "dry_run": args.dry_run,
        "topics_seen": len(topics),
        "topics_attempted": len(archive_results),
        "summary": summarize_results(archive_results),
        "results": archive_results,
        "handoff": {
            "ready_for_ingestion": [
                r["source_ref"]
                for r in archive_results
                if r.get("status") in {"archived_fulltext", "already_fulltext", "sanitized_raw_html"} and r.get("source_ref")
            ],
            "ready_for_agentic_triage": [
                r["source_ref"]
                for r in archive_results
                if r.get("status") in {"archived_fulltext", "already_fulltext", "sanitized_raw_html"} and r.get("source_ref")
            ],
            "requires_historian_review": [],
            "errors": [r for r in archive_results if r.get("status") in {"fulltext_error", "no_posts"}],
        },
    }

    if args.json:
        print_json(payload)
    else:
        print(f"Done. {board_key}: {len(topics)} Themen gesichtet, {len(archive_results)} Ergebnisse.")
        for entry in archive_results[:10]:
            label = entry.get("status") or entry.get("decision")
            print(f"- {entry['topic_id']} | {label} | {entry.get('title')}")
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
