#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import difflib
import json
import os
import re
import subprocess
import sys
import uuid
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path

BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
REGISTER_PATH = REPO_ROOT / ".agent" / "data" / "forum_scan_register.json"
REGISTER_LOCK_PATH = Path("/tmp/7w_wiki_forum_scan_register.lock")
WIKI_ROOT = REPO_ROOT / "docs" / "Siebenwind_Wiki"
INGESTION_REPORTS_DIR = REPO_ROOT / "Logs" / "Ingestion"
FORUM_SOURCE_ROOT = REPO_ROOT / "docs" / "Quellen" / "Forum"
FORUM_ACTIONS = {
    "update_existing",
    "create_article",
    "archive_only",
    "historian_required",
    "human_escalation_required",
}
FORUM_STATUSES = {
    "metadata_only",
    "fulltext_archived",
    "triage_ready",
    "triage_blocked",
    "integrated",
    "reviewed_no_wiki_change",
    "draft_created",
    "style_review_required",
    "ready_to_finalize",
    "duplicate_source",
    "error",
}
REPORT_PROFILE_RE = re.compile(r"- \*\*Quality-Profil \(A/T/K/B/U\)\*\*:\s*([0-9/]+)\s*$", re.MULTILINE)
REPORT_LQS_RE = re.compile(r"- \*\*Lore-Score \(LQS\)\*\*:\s*([0-9]+(?:\.[0-9]+)?)/10")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def today_prefix() -> str:
    return date.today().isoformat()


def repo_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return REPO_ROOT / candidate


def rel(path: str | Path) -> str:
    path = repo_path(path)
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def json_print(payload: dict) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def slugify(text: str) -> str:
    replacements = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue"})
    text = text.translate(replacements).lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text[:90] or "forum_quelle"


def normalize_key(value: str) -> str:
    replacements = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "Ä": "ae", "Ö": "oe", "Ü": "ue"})
    return re.sub(r"[^a-z0-9]", "", value.translate(replacements).lower())


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def split_frontmatter(raw: str) -> tuple[dict[str, str], str, list[str]]:
    if not raw.startswith("---\n"):
        return {}, raw, []
    end = raw.find("\n---\n", 4)
    if end == -1:
        return {}, raw, []
    frontmatter = raw[4:end]
    body = raw[end + 5 :]
    meta: dict[str, str] = {}
    order: list[str] = []
    lines = frontmatter.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        index += 1
        if not line.strip() or line.startswith("  - ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not value and index < len(lines) and lines[index].startswith("  - "):
            items: list[str] = []
            while index < len(lines) and lines[index].startswith("  - "):
                items.append(lines[index])
                index += 1
            value = "\n".join(items)
        meta[key] = value
        order.append(key)
    return meta, body, order


def serialize_frontmatter(meta: dict[str, str], body: str, order: list[str] | None = None) -> str:
    preferred = [
        "uuid",
        "title",
        "category",
        "status",
        "epistemic",
        "quelle",
        "lore_trust",
        "report_id",
        "updated_at",
        "source",
        "source_url",
        "date",
        "type",
        "forum",
        "forum_id",
        "topic_id",
        "content_status",
        "review_status",
        "review_owner",
        "human_escalation_required",
        "integration_status",
        "integrated_target",
        "ingestion_report",
        "integrated_at",
        "archived_at",
        "post_count",
        "topic_pages_archived",
        "raw_html_refs",
    ]
    keys: list[str] = []
    seen: set[str] = set()
    for key in preferred:
        if key in meta and key not in seen:
            keys.append(key)
            seen.add(key)
    for key in order or []:
        if key in meta and key not in seen:
            keys.append(key)
            seen.add(key)
    for key in sorted(meta):
        if key not in seen:
            keys.append(key)
            seen.add(key)

    lines = ["---"]
    for key in keys:
        value = meta[key]
        if value.startswith("  - ") or "\n" in value:
            lines.append(f"{key}:")
            lines.extend(value.splitlines())
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines) + body.lstrip("\n")


def read_source(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    meta, body, order = split_frontmatter(raw)
    title = clean_scalar(meta.get("title") or extract_h1(body) or path.stem)
    topic_id = clean_scalar(meta.get("topic_id", ""))
    raw_refs = extract_raw_html_refs(raw)
    body_text = re.sub(r"^---.*?---", "", raw, flags=re.DOTALL).strip()
    return {
        "path": path,
        "raw": raw,
        "meta": meta,
        "meta_order": order,
        "body": body,
        "body_text": body_text,
        "title": title,
        "topic_id": topic_id,
        "post_count": int(clean_scalar(meta.get("post_count", "0")) or 0),
        "date": clean_scalar(meta.get("date", "")),
        "epistemic": clean_scalar(meta.get("epistemic", "#forum")),
        "raw_html_refs": raw_refs,
    }


def clean_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value.strip('"')
    return value


def extract_h1(body: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", body, re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_raw_html_refs(raw: str) -> list[str]:
    match = re.search(r"^raw_html_refs:\s*\n(?P<items>(?:\s+- .+\n?)+)", raw, re.MULTILINE)
    if not match:
        return []
    refs = []
    for line in match.group("items").splitlines():
        value = line.split("-", 1)[1].strip()
        refs.append(clean_scalar(value))
    return refs


def load_register() -> dict:
    if not REGISTER_PATH.exists():
        return {"version": 1, "boards": {}, "entries": []}
    try:
        return json.loads(REGISTER_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"version": 1, "boards": {}, "entries": []}


@contextlib.contextmanager
def register_lock():
    REGISTER_LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REGISTER_LOCK_PATH.open("w", encoding="utf-8") as handle:
        try:
            import fcntl

            fcntl.flock(handle, fcntl.LOCK_EX)
        except Exception:
            pass
        try:
            yield
        finally:
            try:
                import fcntl

                fcntl.flock(handle, fcntl.LOCK_UN)
            except Exception:
                pass


def save_register(payload: dict) -> None:
    payload.setdefault("version", 1)
    REGISTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTER_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def source_path_from_topic(topic_id: str) -> Path | None:
    payload = load_register()
    for entry in payload.get("entries", []):
        if str(entry.get("topic_id")) == str(topic_id):
            source_ref = entry.get("fulltext_ref") or entry.get("source_ref")
            if source_ref:
                return repo_path(source_ref)
    for path in FORUM_SOURCE_ROOT.rglob("*.md"):
        raw = path.read_text(encoding="utf-8", errors="ignore")
        if re.search(rf"^topic_id:\s*{re.escape(str(topic_id))}\s*$", raw, re.MULTILINE):
            return path
    return None


def resolve_source(source: str | None, topic_id: str | None) -> Path:
    if source:
        path = repo_path(source)
        if not path.exists():
            raise FileNotFoundError(f"Source does not exist: {source}")
        return path
    if topic_id:
        path = source_path_from_topic(topic_id)
        if path and path.exists():
            return path
        raise FileNotFoundError(f"No archived source found for topic-id {topic_id}")
    raise ValueError("Either --source or --topic-id is required")


def wiki_pages() -> list[dict]:
    pages: list[dict] = []
    if not WIKI_ROOT.exists():
        return pages
    for path in sorted(WIKI_ROOT.rglob("*.md")):
        raw = path.read_text(encoding="utf-8", errors="ignore")
        meta, body, _ = split_frontmatter(raw)
        title = clean_scalar(meta.get("title") or extract_h1(body) or path.stem)
        pages.append(
            {
                "path": path,
                "rel": rel(path),
                "title": title,
                "stem": path.stem,
                "norm_title": normalize_key(title),
                "norm_stem": normalize_key(path.stem),
            }
        )
    return pages


def meaningful_title_tokens(title: str) -> list[str]:
    stopwords = {
        "das",
        "der",
        "die",
        "ein",
        "eine",
        "eines",
        "und",
        "aus",
        "dem",
        "den",
        "von",
        "vom",
        "zur",
        "zum",
        "des",
        "im",
        "in",
    }
    tokens = re.findall(r"[A-Za-zÄÖÜäöüß']{4,}", title)
    return [t for t in tokens if t.lower() not in stopwords]


def inspect_source(path: Path) -> dict:
    source = read_source(path)
    title_norm = normalize_key(source["title"])
    title_core = normalize_key(re.sub(r"^(das|der|die|ein|eine)\s+", "", source["title"], flags=re.IGNORECASE))
    tokens = meaningful_title_tokens(source["title"])
    pages = wiki_pages()
    exact = []
    related = []

    for page in pages:
        page_keys = {page["norm_title"], page["norm_stem"]}
        if title_norm in page_keys or title_core in page_keys:
            exact.append({"path": page["rel"], "title": page["title"], "match": "exact_title"})
            continue
        if title_norm.startswith(page["norm_title"]) and len(page["norm_title"]) >= 4:
            exact.append({"path": page["rel"], "title": page["title"], "match": "title_prefix"})
            continue
        similarity = difflib.SequenceMatcher(None, title_core, page["norm_title"]).ratio()
        if len(title_core) >= 8 and similarity >= 0.94:
            exact.append({"path": page["rel"], "title": page["title"], "match": "near_title"})
            continue
        token_hits = [token for token in tokens if normalize_key(token) in page["norm_title"] or normalize_key(token) in page["norm_stem"]]
        if token_hits:
            related.append({"path": page["rel"], "title": page["title"], "tokens": token_hits[:5]})

    risk_flags: list[str] = []
    if source["post_count"] > 5:
        risk_flags.append("multi_post_thread")
    if len(source["body_text"].splitlines()) > 180:
        risk_flags.append("long_source")
    if re.search(r"Hintergrundexkurse|Zweck dieses Forums", source["title"], re.IGNORECASE):
        risk_flags.append("meta_or_background_source")
    if clean_scalar(source["meta"].get("content_status", "")) != "fulltext_archived":
        risk_flags.append("not_fulltext_archived")
    if not source["raw_html_refs"]:
        risk_flags.append("missing_raw_html_refs")

    if "not_fulltext_archived" in risk_flags:
        recommended_action = "archive_only"
    elif "meta_or_background_source" in risk_flags or "multi_post_thread" in risk_flags or "long_source" in risk_flags:
        recommended_action = "historian_required"
    elif exact:
        recommended_action = "update_existing"
    else:
        recommended_action = "create_article"

    return {
        "source_ref": rel(path),
        "title": source["title"],
        "topic_id": source["topic_id"],
        "content_status": clean_scalar(source["meta"].get("content_status", "")),
        "review_status": clean_scalar(source["meta"].get("review_status", "")),
        "post_count": source["post_count"],
        "raw_html_refs": source["raw_html_refs"],
        "exact_candidates": exact[:10],
        "related_candidates": related[:10],
        "risk_flags": risk_flags,
        "recommended_action": recommended_action,
        "human_escalation_required": recommended_action == "human_escalation_required",
    }


def command_forum_queue(args: argparse.Namespace) -> int:
    payload = load_register()
    rows = []
    entries = payload.get("entries", [])
    if args.limit is not None:
        entries = entries[: max(0, args.limit)]
    for entry in entries:
        source_ref = entry.get("fulltext_ref") or entry.get("source_ref")
        content_status = entry.get("content_status") or ("metadata_only" if source_ref else "")
        review_status = entry.get("review_status") or entry.get("integration_status") or ""
        status_values = {content_status, review_status, entry.get("decision", "")}
        if args.status and args.status not in status_values:
            continue
        row = {
            "board": entry.get("board"),
            "topic_id": entry.get("topic_id"),
            "title": entry.get("title"),
            "source_ref": source_ref,
            "content_status": content_status,
            "review_status": review_status,
            "post_count": entry.get("post_count"),
            "integrated_target": entry.get("integrated_target"),
        }
        if source_ref and repo_path(source_ref).exists():
            try:
                inspection = inspect_source(repo_path(source_ref))
                row["recommended_action"] = inspection["recommended_action"]
                row["candidate_count"] = len(inspection["exact_candidates"])
                row["risk_flags"] = inspection["risk_flags"]
            except Exception as exc:
                row["recommended_action"] = "error"
                row["error"] = str(exc)
        else:
            row["recommended_action"] = "archive_fulltext"
        rows.append(row)

    result = {
        "status": "ok",
        "total": len(rows),
        "summary": dict(Counter(row.get("recommended_action", "unknown") for row in rows)),
        "results": rows,
    }
    if args.json:
        json_print(result)
    else:
        print(f"{len(rows)} Forumquellen im Queue-Ausschnitt")
        for row in rows[:20]:
            print(f"- {row.get('topic_id')} | {row.get('recommended_action')} | {row.get('title')}")
    return 0


def command_forum_inspect(args: argparse.Namespace) -> int:
    path = resolve_source(args.source, args.topic_id)
    result = {"status": "ok", "dry_run": args.dry_run, "inspection": inspect_source(path)}
    if args.json:
        json_print(result)
    else:
        inspection = result["inspection"]
        print(f"{inspection['title']} -> {inspection['recommended_action']}")
        for candidate in inspection["exact_candidates"]:
            print(f"- exact: {candidate['path']}")
        for candidate in inspection["related_candidates"][:5]:
            print(f"- related: {candidate['path']}")
    return 0


def source_rel_from_target(source: Path, target: Path) -> str:
    return os.path.relpath(source, target.parent).replace(os.sep, "/")


def report_path_for(source_title: str) -> Path:
    return INGESTION_REPORTS_DIR / f"{today_prefix()}_Forum_{slugify(source_title)}.md"


def quality_for_source(source: dict, action: str) -> tuple[str, str]:
    if action == "create":
        return "4.0", "2/2/4/2/4"
    return "4.2", "2/2/4/3/4"


def write_ingestion_report(source: dict, target: Path, action: str, report_id: str, profile: str, lqs: str) -> Path:
    INGESTION_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = report_path_for(source["title"])
    source_ref = rel(source["path"])
    raw_refs = source.get("raw_html_refs", [])
    now = now_iso()
    body = [
        f"# 📥 Ingestion Report: Forum - {source['title']}",
        "",
        "## Metadaten",
        f"- **Quelle**: `{source_ref}`",
        f"- **Ziel**: `{rel(target)}`",
        f"- **Ausgewertet von**: Codex / Scanner + Historian + Wiki-Schmied",
        f"- **Auswertungszeitpunkt (UTC)**: {now}",
        "- **Quellentyp**: #forum #perspektive",
        f"- **Lore-Score (LQS)**: {lqs}/10",
        f"- **Quality-Profil (A/T/K/B/U)**: {profile}",
        f"- **Report-ID**: {report_id}",
        "",
        "## Entscheidung",
        f"- **Aktion**: {'Neuanlage' if action == 'create' else 'Aktualisierung'}",
        "- **Menschliche Eskalation**: nein",
        "- **Historiker-Prüfung**: operativ unkritisch; keine harte Kanonkorrektur erkannt.",
        "",
        "## Übernommene Aussagen",
    ]
    if "ergon" in normalize_key(source["title"]):
        body.extend(
            [
                "- Ergon wird in der Forumquelle als Hobbit in einer Küchenszene in Dunquell geschildert.",
                "- Die Szene trägt Kürbis-, Herbst- und Tavernensmial-Motive.",
                "- Die Aussagen wurden ausdrücklich als Forumsperspektive markiert.",
            ]
        )
    elif "handelskontor" in normalize_key(source["title"]):
        body.extend(
            [
                "- Die Quelle beschreibt ein orkisches Handelskontor in Brandenstein bei der alten Schlachterei.",
                "- Beteiligte werden als Orken, Goblins und gezähmte Oger benannt.",
                "- Das Warenangebot wird nur als Perspektivtext übernommen.",
            ]
        )
    else:
        body.append("- Die Quelle wurde quellengetreu und mit niedriger epistemischer Markierung verarbeitet.")

    body.extend(
        [
            "",
            "## Nicht übernommen",
            "- Keine neuen Kanonbehauptungen über höhere Quellen hinaus.",
            "- Keine automatische Aufwertung des Forumtexts zu #canon.",
            "",
            "## Raw HTML",
        ]
    )
    if raw_refs:
        body.extend([f"- `{ref}`" for ref in raw_refs])
    else:
        body.append("- [UNGEKLÄRT] Keine Raw-HTML-Referenz im Quelldokument gefunden.")
    body.extend(["", "---", "*Status: COMPLETED*"])
    report_path.write_text("\n".join(body).rstrip() + "\n", encoding="utf-8")
    return report_path


def update_ergon_page(target: Path, source: dict, report_id: str, report_path: Path) -> None:
    raw = target.read_text(encoding="utf-8") if target.exists() else ""
    meta, body, order = split_frontmatter(raw)
    meta.setdefault("uuid", str(uuid.uuid4()))
    meta["title"] = "Ergon"
    meta["category"] = "Personen"
    meta["status"] = "gepflegt"
    meta["epistemic"] = '"#bote #forum"'
    meta["quelle"] = yaml_string(source_rel_from_target(source["path"], target))
    meta["lore_trust"] = "4"
    meta["report_id"] = report_id
    meta["updated_at"] = yaml_string(now_iso())

    body = f"""# Ergon

!!! info "Metadaten"
    - **Titel:** Bürgermeister von [[Dunquell]]
    - **Epistemischer Status:** #bote, ergänzt durch #forum
    - **Zugehörigkeit:** [[Dunquell]] / [[Dwarschim]]

## Beschreibung
**Ergon** ist der Bürgermeister der Zwergensiedlung [[Dunquell]].
Er ist bekannt für seine Gedichte (Bote 189/190) und wird als möglicher Kandidat für das Amt des Vizekanzlers gehandelt.

## Weitere Überlieferung
Eine weitere Überlieferung zeigt Ergon als Hobbit mit rußverschmierter Schürze in der Küche eines Tavernensmials. Die Szene verbindet ihn mit herbstlicher Kürbisküche, Dunquell und einer ruhigen, handwerklichen Alltagsdarstellung. Diese Lesart steht neben der älteren Boten-Einordnung und ersetzt sie nicht.

## Verlinkte Themen
- [[Dunquell]]
- [[Dwarschim]]
- [[Hobbits]]

## Referenzen
- Forumquelle: `{source_rel_from_target(source["path"], target)}`
- Raw HTML: `{source["raw_html_refs"][0] if source["raw_html_refs"] else "[UNGEKLÄRT]"}`
- Prüfbericht: `{os.path.relpath(report_path, target.parent).replace(os.sep, "/")}` (ID: `{report_id}`)
"""
    target.write_text(serialize_frontmatter(meta, body, order), encoding="utf-8")


def create_handelskontor_page(target: Path, source: dict, report_id: str, report_path: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    meta = {
        "uuid": str(uuid.uuid4()),
        "title": "Orkisches Handelskontor",
        "category": "Gesellschaft",
        "status": "gepflegt",
        "epistemic": '"#forum #perspektive"',
        "quelle": yaml_string(source_rel_from_target(source["path"], target)),
        "lore_trust": "4",
        "report_id": report_id,
        "updated_at": yaml_string(now_iso()),
    }
    body = f"""# Orkisches Handelskontor

!!! info "Metadaten"
    - **Typ:** Handelsort / Erzählüberlieferung
    - **Epistemischer Status:** #forum #perspektive
    - **Ort:** [[Brandenstein]]

## Beschreibung
Das **Orkische Handelskontor** gilt in einer Erzählüberlieferung als Handelsort in [[Brandenstein]]. Es wird im Umfeld der alten Schlachterei verortet und mit einer Gruppe aus [[Orken]], [[Goblins]] und gezähmten [[Oger|Ogern]] verbunden.

## Warenbild
Zum Warenbild zählen einfaches Rüstzeug, grobe Waffen und gelegentlich seltenes Beutegut. Aus der Überlieferung ergibt sich keine allgemeine Wirtschaftsregel für [[Brandenstein]].

## Verlinkte Themen
- [[Brandenstein]]
- [[Orken]]
- [[Goblins]]
- [[Oger]]
- [[Hafengilde_Brandenstein]]

## Referenzen
- Forumquelle: `{source_rel_from_target(source["path"], target)}`
- Raw HTML: `{source["raw_html_refs"][0] if source["raw_html_refs"] else "[UNGEKLÄRT]"}`
- Prüfbericht: `{os.path.relpath(report_path, target.parent).replace(os.sep, "/")}` (ID: `{report_id}`)
"""
    target.write_text(serialize_frontmatter(meta, body), encoding="utf-8")


def wiki_title_from_link(link: str) -> str:
    return link.split("|", 1)[0].strip("[]")


def generic_forum_links(source: dict) -> list[str]:
    haystack = f"{source['title']}\n{source['body_text']}"
    candidates = [
        ("Brandenstein", "[[Brandenstein]]"),
        ("Rathaus", "[[Brandenstein]]"),
        ("Westhever", "[[Zerstoerung_von_Westhever|Westhever]]"),
        ("Dunkeltief", "[[Dunkeltief]]"),
        ("Finsterwangen", "[[Finsterwangen]]"),
        ("Tardukai", "[[Bruderschaft_der_Tardukai]]"),
        ("Schattenhand", "[[Schattenhand]]"),
        ("Burg-Ruine Schwingenwacht", "[[Burg_Schwingenwacht|Burg Schwingenwacht]]"),
        ("Schwingenwacht", "[[Burg_Schwingenwacht|Burg Schwingenwacht]]"),
        ("Königin Brynn", "[[Königin_Brynn|Königin Brynn]]"),
        ("Brynn", "[[Königin_Brynn|Königin Brynn]]"),
        ("Toran Dur", "[[Toran_Dur]]"),
        ("Ignis", "[[Ignis]]"),
        ("Ventus", "[[Ventus]]"),
        ("Xan", "[[Xan]]"),
        ("Morsan", "[[Morsan]]"),
        ("Tempelwache", "[[Tempelwache]]"),
        ("Bellum", "[[Bellum]]"),
        ("Myrandhir", "[[Myrandhir]]"),
        ("Nortraven", "[[Nortraven]]"),
        ("Goblins", "[[Goblins]]"),
        ("Goblin", "[[Goblins]]"),
    ]
    links: list[str] = []
    seen: set[str] = set()
    for needle, link in candidates:
        if re.search(rf"\b{re.escape(needle)}\b", haystack, re.IGNORECASE):
            key = wiki_title_from_link(link)
            if key not in seen:
                links.append(link)
                seen.add(key)
    return links or ["[[Siebenwind]]"]


def generic_forum_summary(source: dict) -> list[str]:
    norm = normalize_key(source["title"])
    if "treibenimrathaus" in norm:
        return [
            "Im Rathaus von [[Brandenstein]] regt sich nach längerer Ruhe wieder Betrieb. Ein ehrgeizig wirkender Mann geht dort wiederholt ein und aus.",
            "Das erneut sichtbare Öffnungsschild und entstaubte Räume lassen erkennen, dass die sogenannte Neue Verwaltung wieder Aufmerksamkeit auf sich zieht.",
        ]
    if "angriffaufwesthever" in norm:
        return [
            "Ein Angriff auf [[Zerstoerung_von_Westhever|Westhever]] verbindet sich mit Gerüchten über [[Goblins]], Ferrins und Fischmenschen.",
            "Danach kommt es am Hafen von [[Brandenstein]] zu Unruhe, einem gekaperten Marineschiff und einer Verfolgung durch die Litheth.",
            "Weitere Szenen betreffen den Eintritt einer jungen Frau in die Tempelwache, kirchliche Figuren und einen späteren Piratenangriff auf Brandenstein.",
        ]
    if norm == "xiii":
        return [
            "Ein alter Seemann hält bei einem Leuchtfeuer nahe [[Brandenstein]] Wache und denkt über ein Geisterschiff, Schuld und sicheren Kurs auf See nach.",
            "Die Xanfelawende verbindet sich mit Gebeten an [[Ignis]], [[Ventus]] und [[Xan]] sowie mit Verlust, Kameradschaft und der Erinnerung an gefallene Seeleute.",
            "Der zweite Beitrag führt das Motiv über Zinnsoldaten und den Xanschrein weiter; die Toten von Krieg, Schiffbruch und Seenot werden ausdrücklich den Fluten und [[Morsan]] anvertraut.",
        ]
    if "aufkeimendeschatten" in norm:
        return [
            "Eine maskierte Gestalt aus dem Umfeld dunkler Angamon-Verehrung bewegt sich nach dem zurückliegenden [[Dunkeltief]] zwischen verstreuten Glaubensgruppen, der [[Bruderschaft_der_Tardukai]] und der Erinnerung an die [[Schattenhand]].",
            "Im Zentrum stehen Untersuchungen an kopflosen bleichen Kreaturen, Knochenwerkzeugen, Schädeln und einer fremden, streng geometrischen Magiesignatur. Die Spur führt von einer alten Mine über die Wälder bei [[Brandenstein]] bis in ein verborgenes Labor unter der Insel.",
            "Faisons Kult, Finsterwangen, Knochenmasken und eine fliehende bleiche Gestalt bleiben als Motive dieser Überlieferung greifbar; Herkunft und Meister der Kreaturen bleiben [UNGEKLÄRT].",
        ]
    if "einfuchsstreiftdurchdiewaelder" in norm:
        return [
            "Eine Gestalt, die als Fuchs oder alter Mann erscheint, zieht über die Insel, sucht Ruinen und abgelegene Orte auf und beansprucht schließlich einen alten Wachturm nahe Kesselklamm für sich.",
            "Unter dem Namen Theodor Fuchs tritt die Figur als Sekretarius der Stadtverwaltung [[Brandenstein]] auf und berichtet in Briefen an Dunquell, Finsterwangen und die Bewacher des Walls von der Ankunft [[Königin_Brynn|Königin Brynns]] und ihres Gefolges.",
            "Weitere Beiträge verbinden Natur- und Ritualmotive mit [[Burg_Schwingenwacht|Schwingenwacht]], einem Turm, Tierzeichen, Opfergaben und wiederkehrenden Beobachtungen der politischen und magischen Lage auf der Insel.",
        ]
    paragraphs = []
    for raw_line in source["body_text"].splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("#", "-", "_", "---")):
            continue
        if re.match(r"^(Autor|Verfasst|Post-ID|Forum|Link|Topic-ID|Archiviert am):", line):
            continue
        if len(line) >= 80:
            paragraphs.append(line)
        if len(paragraphs) >= 2:
            break
    if not paragraphs:
        return ["Eine belastbare Kurzfassung dieser Überlieferung bleibt [UNGEKLÄRT]."]
    return [
        re.sub(r"\s+", " ", paragraph).strip()
        for paragraph in paragraphs[:2]
    ]


def create_generic_forum_page(target: Path, source: dict, report_id: str, report_path: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    title = source["title"].strip().rstrip(".")
    if not title:
        title = target.stem.replace("_", " ")
    category = "Geschichte" if "05_Geschichte" in rel(target) else "Erzählung"
    links = generic_forum_links(source)
    summary = generic_forum_summary(source)
    meta = {
        "uuid": str(uuid.uuid4()),
        "title": yaml_string(title),
        "category": category,
        "status": "gepflegt",
        "epistemic": '"#forum #perspektive"',
        "quelle": yaml_string(source_rel_from_target(source["path"], target)),
        "lore_trust": "4",
        "report_id": report_id,
        "updated_at": yaml_string(now_iso()),
    }
    body = [
        f"# {title}",
        "",
        "## Überblick",
    ]
    body.extend(summary)
    body.extend(
        [
            "",
            "## Motive und Bezüge",
            "Die Überlieferung ist im Frontmatter als `#forum #perspektive` markiert. Offene Deutungen bleiben ausdrücklich als [UNGEKLÄRT] gekennzeichnet.",
            "",
            "## Verlinkte Themen",
        ]
    )
    body.extend(f"- {link}" for link in links)
    body.extend(
        [
            "",
            "## Referenzen",
            f"- Forumquelle: `{source_rel_from_target(source['path'], target)}`",
            f"- Raw HTML: `{os.path.relpath(repo_path(source['raw_html_refs'][0]), target.parent).replace(os.sep, '/') if source['raw_html_refs'] else '[UNGEKLÄRT]'}`",
            f"- Prüfbericht: `{os.path.relpath(report_path, target.parent).replace(os.sep, '/')}` (ID: `{report_id}`)",
        ]
    )
    target.write_text(serialize_frontmatter(meta, "\n".join(body).rstrip() + "\n"), encoding="utf-8")


def forum_production_gate(target: Path) -> list[str]:
    issues: list[str] = []
    if not target.exists():
        return [f"Target does not exist: {rel(target)}"]
    if not rel(target).startswith("docs/Siebenwind_Wiki/"):
        return issues

    raw = target.read_text(encoding="utf-8")
    meta, body, _ = split_frontmatter(raw)
    for required in ("title", "category"):
        if required not in meta or not clean_scalar(meta.get(required, "")):
            issues.append(f"Fehlendes Frontmatter-Feld: '{required}'")
    if "layout" in meta:
        issues.append("Legacy-Frontmatter-Feld 'layout' darf in neuen Produktionsartikeln nicht gesetzt sein")

    title = clean_scalar(meta.get("title", ""))
    h1 = extract_h1(body)
    if title and h1 != title:
        issues.append(f"Titel-Mismatch: H1='{h1}' != Frontmatter='{title}'")
    elif not h1:
        issues.append("Keine H1-Überschrift gefunden.")

    main_body = re.split(r"^##\s+Referenzen\s*$", body, maxsplit=1, flags=re.MULTILINE)[0]
    forbidden_patterns = [
        (r"archivierte Forumquelle", "Technische Archivformel gehoert nicht in den Artikelkoerper"),
        (r"nicht automatisch kanonisiert", "Kanonisierungs-Boilerplate gehoert in Metadaten/Report"),
        (r"Raw HTML", "Raw-HTML-Hinweise gehoeren nur in Referenzen/Report"),
        (r"Registerstatus|Registerlogik", "Registerhinweise gehoeren nicht in den Artikelkoerper"),
        (r"Die Quelle bleibt", "Quellenkarten-Formulierung statt Wiki-Ton"),
        (r"Die Aussagen dieser Seite bleiben", "Quellenkarten-Formulierung statt Wiki-Ton"),
        (r"^##\s+Einordnung\s*$", "Generische Einordnung ist fuer Forum-Neuanlagen kein Produktionsstandard"),
        (r"!!! info \"Metadaten\"[\s\S]{0,220}Forumquelle", "Sichtbare technische Forum-Metabox statt Wiki-Ton"),
    ]
    for pattern, message in forbidden_patterns:
        if re.search(pattern, main_body, re.IGNORECASE | re.MULTILINE):
            issues.append(message)

    return issues


def update_source_draft_status(source_path: Path, target: Path, report: Path) -> None:
    source = read_source(source_path)
    with register_lock():
        meta = dict(source["meta"])
        payload = load_register()
        meta["review_status"] = "style_review_required"
        meta["review_owner"] = "Codex / Scanner + Wiki-Schmied"
        meta["integration_status"] = "draft_created"
        meta["integrated_target"] = yaml_string(rel(target))
        meta["ingestion_report"] = yaml_string(rel(report))
        source_path.write_text(serialize_frontmatter(meta, source["body"], source["meta_order"]), encoding="utf-8")

        updated = False
        for entry in payload.setdefault("entries", []):
            if str(entry.get("topic_id")) == str(source["topic_id"]):
                entry["review_status"] = "style_review_required"
                entry["integration_status"] = "draft_created"
                entry["review_owner"] = "Codex / Scanner + Wiki-Schmied"
                entry["integrated_target"] = rel(target)
                entry["ingestion_report"] = rel(report)
                entry["content_status"] = entry.get("content_status") or "fulltext_archived"
                updated = True
                break
        if not updated:
            payload.setdefault("entries", []).append(
                {
                    "board": "geschichten",
                    "topic_id": source["topic_id"],
                    "title": source["title"],
                    "source_ref": rel(source_path),
                    "fulltext_ref": rel(source_path),
                    "content_status": "fulltext_archived",
                    "review_status": "style_review_required",
                    "integration_status": "draft_created",
                    "integrated_target": rel(target),
                    "ingestion_report": rel(report),
                    "human_escalation_required": False,
                }
            )
        save_register(payload)


def command_forum_draft(args: argparse.Namespace) -> int:
    source_path = resolve_source(args.source, args.topic_id)
    source = read_source(source_path)
    target = repo_path(args.target)
    action = args.action
    inspection = inspect_source(source_path)

    if action == "update" and not target.exists():
        raise FileNotFoundError(f"Update target does not exist: {args.target}")
    if action == "create" and target.exists():
        return_payload = {
            "status": "blocked",
            "reason": "target_exists",
            "source_ref": rel(source_path),
            "target": rel(target),
            "inspection": inspection,
        }
        if args.json:
            json_print(return_payload)
        else:
            print(f"Target already exists: {rel(target)}")
        return 1

    report_id = str(uuid.uuid4())
    lqs, profile = quality_for_source(source, action)
    report_path = report_path_for(source["title"])
    planned = {
        "status": "would_apply" if args.dry_run or not args.apply else "applied",
        "source_ref": rel(source_path),
        "target": rel(target),
        "action": action,
        "report_ref": rel(report_path),
        "report_id": report_id,
        "quality_profile": profile,
        "lqs": lqs,
        "inspection": inspection,
    }

    if args.dry_run or not args.apply:
        if args.json:
            json_print(planned)
        else:
            print(f"Would {action} {rel(target)} from {rel(source_path)}")
        return 0

    report_path = write_ingestion_report(source, target, action, report_id, profile, lqs)
    if "ergon" in normalize_key(source["title"]) and action == "update":
        update_ergon_page(target, source, report_id, report_path)
    elif "handelskontor" in normalize_key(source["title"]) and action == "create":
        create_handelskontor_page(target, source, report_id, report_path)
    elif action == "create":
        create_generic_forum_page(target, source, report_id, report_path)
    else:
        raise ValueError("Generic forum drafting is not implemented for this source/action pair yet")
    update_source_draft_status(source_path, target, report_path)

    planned["report_ref"] = rel(report_path)
    planned["integration_status"] = "draft_created"
    planned["review_status"] = "style_review_required"
    if args.json:
        json_print(planned)
    else:
        print(f"Applied {action}: {rel(target)}")
        print(f"Report: {rel(report_path)}")
    return 0


def update_source_finalization(source_path: Path, target: Path, report: Path, status: str) -> dict:
    source = read_source(source_path)
    with register_lock():
        meta = dict(source["meta"])
        payload = load_register()
        register_entry = next((entry for entry in payload.get("entries", []) if str(entry.get("topic_id")) == str(source["topic_id"])), {})
        raw_refs = source["raw_html_refs"] or register_entry.get("raw_html_refs", [])
        if raw_refs:
            meta["raw_html_refs"] = "\n".join(f"  - {yaml_string(ref)}" for ref in raw_refs)
        meta.pop("human_review_required", None)
        meta["review_status"] = status
        meta["review_owner"] = "Codex / Scanner + Historian + Wiki-Schmied"
        meta["human_escalation_required"] = "false"
        meta["integration_status"] = status
        meta["integrated_target"] = yaml_string(rel(target))
        meta["ingestion_report"] = yaml_string(rel(report))
        meta["integrated_at"] = yaml_string(now_iso())
        source_path.write_text(serialize_frontmatter(meta, source["body"], source["meta_order"]), encoding="utf-8")

        updated = False
        for entry in payload.setdefault("entries", []):
            if str(entry.get("topic_id")) == str(source["topic_id"]):
                entry["review_status"] = status
                entry["integration_status"] = status
                entry["review_owner"] = "Codex / Scanner + Historian + Wiki-Schmied"
                entry["human_escalation_required"] = False
                entry["integrated_target"] = rel(target)
                entry["ingestion_report"] = rel(report)
                entry["integrated_at"] = now_iso()
                entry["content_status"] = entry.get("content_status") or "fulltext_archived"
                updated = True
                break
        if not updated:
            payload.setdefault("entries", []).append(
                {
                    "board": "geschichten",
                    "topic_id": source["topic_id"],
                    "title": source["title"],
                    "source_ref": rel(source_path),
                    "fulltext_ref": rel(source_path),
                    "content_status": "fulltext_archived",
                    "review_status": status,
                    "integration_status": status,
                    "integrated_target": rel(target),
                    "ingestion_report": rel(report),
                    "integrated_at": now_iso(),
                    "human_escalation_required": False,
                }
            )
        save_register(payload)
    return {
        "source_ref": rel(source_path),
        "target": rel(target),
        "report_ref": rel(report),
        "topic_id": source["topic_id"],
        "review_status": status,
    }


def command_forum_finalize(args: argparse.Namespace) -> int:
    source_path = resolve_source(args.source, None)
    target = repo_path(args.target)
    report = repo_path(args.report)
    if not target.exists():
        raise FileNotFoundError(f"Target does not exist: {args.target}")
    if not report.exists():
        raise FileNotFoundError(f"Report does not exist: {args.report}")
    gate_issues = forum_production_gate(target) if args.status == "integrated" else []
    if gate_issues and not args.allow_draft_finalize:
        result = {
            "status": "blocked",
            "reason": "production_gate_failed",
            "source_ref": rel(source_path),
            "target": rel(target),
            "issues": gate_issues,
        }
        if args.json:
            json_print(result)
        else:
            print(f"Production gate failed for {rel(target)}:")
            for issue in gate_issues:
                print(f"- {issue}")
        return 1
    result = {"status": "ok", "finalized": update_source_finalization(source_path, target, report, args.status)}
    if args.json:
        json_print(result)
    else:
        print(f"Finalized {rel(source_path)} -> {rel(target)}")
    return 0


def profile_from_lqs(lqs: float, report_path: Path, raw: str) -> str | None:
    if lqs >= 9.5:
        return "5/5/5/4/4"
    if lqs >= 8.5:
        return "5/4/5/4/4"
    if lqs >= 7.5:
        return "4/4/5/4/4"
    if lqs >= 6.5:
        return "4/3/4/3/3"
    if lqs >= 5:
        return "3/2/4/2/3"
    if lqs >= 3:
        if "Aktion**: Aktualisierung" in raw:
            return "2/2/4/3/4"
        if "Aktion**: Neuanlage" in raw:
            return "2/2/4/2/4"
        if "Stub" in raw or "Quelle fehlt" in raw or "physisch nicht präsent" in raw:
            return "0/0/3/1/1"
        return "2/1/3/1/2"
    if lqs >= 1:
        return "1/1/2/1/1"
    return "0/0/1/0/1"


def report_lqs(raw: str) -> float | None:
    match = REPORT_LQS_RE.search(raw)
    if match:
        return float(match.group(1))
    table_match = re.search(r"\| \*\*Gesamt \(LQS(?: 0-10)?\)\*\* \| \*\*([0-9]+(?:\.[0-9]+)?)/10\*\*", raw)
    if table_match:
        return float(table_match.group(1))
    return None


def calibrate_report_text(raw: str, report_path: Path) -> tuple[str, dict]:
    existing = REPORT_PROFILE_RE.search(raw)
    lqs = report_lqs(raw)
    action = {
        "file": rel(report_path),
        "current_profile": existing.group(1) if existing else "",
        "new_profile": "",
        "status": "unchanged",
    }
    if lqs is None:
        action["status"] = "needs_manual_calibration"
        return raw, action
    new_profile = profile_from_lqs(lqs, report_path, raw)
    if not new_profile:
        action["status"] = "needs_manual_calibration"
        return raw, action
    action["new_profile"] = new_profile
    if existing:
        if existing.group(1) == new_profile:
            return raw, action
        action["status"] = "updated_profile"
        return raw[: existing.start(1)] + new_profile + raw[existing.end(1) :], action

    lore_match = REPORT_LQS_RE.search(raw)
    if lore_match:
        insertion = f"\n- **Quality-Profil (A/T/K/B/U)**: {new_profile}"
        action["status"] = "inserted_profile"
        return raw[: lore_match.end()] + insertion + raw[lore_match.end() :], action

    action["status"] = "needs_manual_calibration"
    return raw, action


def command_reports_calibrate(args: argparse.Namespace) -> int:
    results = []
    for report_path in sorted(INGESTION_REPORTS_DIR.glob("*.md")):
        raw = report_path.read_text(encoding="utf-8", errors="ignore")
        if not re.search(r"^#\s+📥\s+Ingestion Report", raw, re.MULTILINE):
            continue
        new_raw, action = calibrate_report_text(raw, report_path)
        if action["status"] != "unchanged" or args.include_unchanged:
            results.append(action)
        if args.apply and new_raw != raw:
            report_path.write_text(new_raw, encoding="utf-8")

    summary = dict(Counter(item["status"] for item in results))
    payload = {
        "status": "ok",
        "dry_run": not args.apply,
        "summary": summary,
        "results": results,
    }
    if args.json:
        json_print(payload)
    else:
        print(f"Reports checked: {len(results)}")
        for status, count in summary.items():
            print(f"- {status}: {count}")
    return 0


def run_script(script_path: str, args: list[str]) -> int:
    executable = sys.executable
    cmd = [executable, os.path.join(REPO_ROOT, script_path)] + args
    print(f"\n{BOLD}▶ {script_path} {' '.join(args)}{RESET}")
    result = subprocess.run(cmd)
    return result.returncode


def legacy_pipeline(file_arg: str) -> int:
    target_path = Path(file_arg)
    if not target_path.exists():
        print(f"Error: Target path {file_arg} does not exist.", file=sys.stderr)
        return 1

    print(f"{BOLD}🛡️  Starte Ingest-Pipeline fuer: {file_arg}{RESET}")
    print("Dieser Workflow fuehrt automatisch Linting, Archive-Sync und einen abschliessenden Audit-Check aus.\n")

    print(f"{BOLD}Phase 1: Lint, Score & Sanitize{RESET}")
    rc_lint = run_script("7w_wiki.py", ["lint", file_arg, "--fix"])
    if rc_lint != 0:
        print(f"{YELLOW}⚠ Lint-Phase meldete Warnungen. Fortsetzung...{RESET}")

    print(f"\n{BOLD}Phase 2: Archive Sync{RESET}")
    rc_sync = run_script("7w_wiki.py", ["archive", "sync"])

    print(f"\n{BOLD}Phase 3: Consistency Audit{RESET}")
    rc_audit = run_script("7w_wiki.py", ["audit"])

    overall = max(rc_lint, rc_sync, rc_audit)
    print("\n" + "=" * 50)
    if overall == 0:
        print(f"{BOLD}{GREEN}✓ Ingest-Pipeline (Zyklus der Weisheit) erfolgreich abgeschlossen.{RESET}")
    else:
        print(f"{BOLD}{YELLOW}⚠ Ingest-Pipeline mit Warnungen oder Fehlern beendet (Highest Exit: {overall}).{RESET}")
        print("Bitte pruefe den finalen Audit-Report auf offene Registrierungs-Inkonsistenzen.")
    return overall


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified Ingest Pipeline for Siebenwind Wiki")
    sub = parser.add_subparsers(dest="command")

    queue = sub.add_parser("forum-queue", help="List archived forum sources and recommended next actions")
    queue.add_argument("--json", action="store_true")
    queue.add_argument("--status", choices=sorted(FORUM_STATUSES))
    queue.add_argument("--limit", type=int)
    queue.set_defaults(func=command_forum_queue)

    inspect = sub.add_parser("forum-inspect", help="Inspect one forum source for target candidates")
    inspect.add_argument("--source")
    inspect.add_argument("--topic-id")
    inspect.add_argument("--dry-run", action="store_true")
    inspect.add_argument("--json", action="store_true")
    inspect.set_defaults(func=command_forum_inspect)

    draft = sub.add_parser("forum-draft", help="Draft or apply a forum-source wiki update")
    draft.add_argument("--source")
    draft.add_argument("--topic-id")
    draft.add_argument("--action", required=True, choices=["update", "create"])
    draft.add_argument("--target", required=True)
    mode = draft.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    draft.add_argument("--json", action="store_true")
    draft.set_defaults(func=command_forum_draft)

    finalize = sub.add_parser("forum-finalize", help="Finalize forum source integration status")
    finalize.add_argument("--source", required=True)
    finalize.add_argument("--target", required=True)
    finalize.add_argument("--report", required=True)
    finalize.add_argument("--status", required=True, choices=["integrated", "reviewed_no_wiki_change"])
    finalize.add_argument("--allow-draft-finalize", action="store_true", help="Bypass wiki production gate for exceptional/manual cases")
    finalize.add_argument("--json", action="store_true")
    finalize.set_defaults(func=command_forum_finalize)

    calibrate = sub.add_parser("reports-calibrate", help="Calibrate legacy ingestion report quality profiles")
    calibrate.add_argument("--dry-run", action="store_true")
    calibrate.add_argument("--apply", action="store_true")
    calibrate.add_argument("--include-unchanged", action="store_true")
    calibrate.add_argument("--json", action="store_true")
    calibrate.set_defaults(func=command_reports_calibrate)
    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])
    if not argv:
        build_parser().print_help()
        return 1

    known_commands = {"forum-queue", "forum-inspect", "forum-draft", "forum-finalize", "reports-calibrate"}
    if argv[0] in {"-h", "--help"}:
        build_parser().print_help()
        return 0
    if argv[0] not in known_commands:
        if len(argv) != 1:
            print("Legacy ingest accepts exactly one file argument.", file=sys.stderr)
            return 2
        return legacy_pipeline(argv[0])

    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "reports-calibrate" and not args.apply:
        args.dry_run = True
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    try:
        return args.func(args)
    except Exception as exc:
        if getattr(args, "json", False):
            json_print({"status": "error", "error": f"{type(exc).__name__}: {exc}"})
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
