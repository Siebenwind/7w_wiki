"""MkDocs hooks for reader metadata and the one static search index.

Executed only as part of ./7w_wiki.py pages build/validate.
"""
from __future__ import annotations

import hashlib
import html
import json
import posixpath
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote
from reader_health import bridge_lifecycle, rendered_links

ROOT = Path(__file__).resolve().parents[2]
records = []
seen_sources = {}
build = {}


def plain(value):
    value = re.sub(r"\[\[([^]|]+)\|([^]]+)\]\]", r"\2", str(value))
    value = re.sub(r"\[\[([^]]+)\]\]", r"\1", value)
    return html.unescape(re.sub(r"<[^>]*>", " ", value)).replace("_", " ").strip()


def on_config(config):
    records.clear()
    seen_sources.clear()
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    build.clear()
    build.update(date=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                 commit=git("rev-parse", "HEAD"), dirty=bool(git("diff", "--name-only")))
    config.extra["reader_build"] = build
    return config


def on_page_content(content, page, config, files):
    src = page.file.src_uri
    kind = "wiki" if src.startswith("Siebenwind_Wiki/") else "quellen" if src.startswith("Quellen/") else "forschung" if src.startswith(("Archiv/", "Ingestion_Reports/")) or src == "forschung.md" else "technik"
    title = plain(page.meta.get("title") or page.title)
    bridge = page.meta.get("bridge_target")
    aliases = page.meta.get("aliases", [])
    if isinstance(aliases, str):
        aliases = [aliases]
    record = {"url": quote(page.url, safe='/%'), "title": title, "kind": kind,
              "aliases": [plain(a) for a in aliases] + [plain(Path(src).stem)],
              "bridge_target": str(bridge or ""), "source": src}
    if kind == "quellen":
        digest = hashlib.sha256(re.sub(r"\s+", " ", plain(content)).encode()).hexdigest()
        if digest in seen_sources:
            record["duplicate_of"] = seen_sources[digest]
        else:
            seen_sources[digest] = page.url
    records.append(record)
    ignored = bool(bridge or record.get("duplicate_of") or src in {"suche.md", "themen.md", "index.md", "neues.md"})
    attrs = 'data-pagefind-ignore="all"' if ignored else f'data-pagefind-body data-pagefind-filter="bereich:{kind}"'
    meta = f'<span hidden data-pagefind-meta="title">{html.escape(title)}</span>'
    notes = ""
    if kind == "wiki" and Path(src).name != "index.md":
        url = config.site_url.rstrip("/") + "/" + page.url
        issue = "https://github.com/Siebenwind/7w_wiki/issues/new?title=" + quote("Hinweis zu " + title) + "&body=" + quote("Artikel: " + url + "\n\nBeobachtung:\n\nQuelle oder Korrekturvorschlag:\n")
        source = page.meta.get("quelle")
        source_note = "Eine zentrale Quellenangabe fehlt. Beachte vorhandene Belege und Hinweise im Text."
        if source:
            source_note = "Eine Quelle ist im Artikel verzeichnet. Die Referenzen im Text erläutern Herkunft und Zusammenhang."
            source_url = None
            if isinstance(source, str):
                if source.startswith(("https://", "http://")):
                    source_url = source
                else:
                    source_file = files.get_file_from_path(posixpath.normpath(posixpath.join(posixpath.dirname(src), source)))
                    if source_file:
                        source_url = config.site_url.rstrip("/") + "/" + quote(source_file.url, safe="/%")
            if source_url:
                source_note = '<a href="' + html.escape(source_url, quote=True) + '">Verzeichnete Originalquelle lesen</a>. Weitere Belege und Einordnungen stehen in den Referenzen des Artikels.'
        notes = f'<aside class="sw-article-context" data-pagefind-ignore><details><summary>Quellen und Einordnung</summary><p>{source_note}</p><p>Kanon, Chronik und persönliche Erzählung sind unterschiedliche Quellenarten. Ein Tag ist kein Nachweis einer abgeschlossenen Prüfung. [UNGEKLÄRT] kennzeichnet offene Fragen.</p></details><a href="{html.escape(issue, quote=True)}">Fehler melden</a></aside>'
    # A text alternative stays available even when Mermaid renders as an SVG.
    def diagram_text(match):
        raw = html.unescape(match.group(2))
        values = re.findall(r'"([^"]+)"\s*:\s*([\d.]+)', raw)
        description = '<ul>' + ''.join('<li>' + html.escape(label) + ': ' + value + '</li>' for label,value in values) + '</ul>' if values else '<pre>' + match.group(2) + '</pre>'
        return match.group(0) + '<details class="sw-diagram-text" data-pagefind-ignore><summary>Diagramm als Text</summary>' + description + '</details>'
    content = re.sub(r'(<pre class="mermaid"><code>)([\s\S]*?)(</code></pre>)', diagram_text, content)
    return f'<div {attrs}>{meta}{content}</div>{notes}'


def on_post_build(config):
    site = Path(config.site_dir)
    lifecycle = bridge_lifecycle()
    if lifecycle['violations']:
        raise RuntimeError('New bridge lifecycle violations: ' + str(lifecycle['violations']))
    links = rendered_links(site, config.site_url)
    (site / 'rendered-links.json').write_text(json.dumps(links, ensure_ascii=False, indent=2), encoding='utf-8')
    targets = {}
    for record in records:
        if record["kind"] != "wiki" or record["bridge_target"]:
            continue
        for key in [record["title"], *record["aliases"]]:
            targets.setdefault(plain(key).casefold(), []).append(record)
    for record in records:
        if record["bridge_target"]:
            key = plain(record["bridge_target"]).strip("[]").casefold()
            matches = targets.get(key, [])
            urls = {r["url"] for r in matches}
            if len(urls) == 1:
                matches[0]["aliases"].extend([record["title"], *record["aliases"]])
    for record in records:
        if record['kind'] == 'wiki' and not record['bridge_target']:
            target = site / unquote(record['url']) / 'index.html'
            if target.is_file():
                raw = target.read_text(encoding='utf-8')
                terms = html.escape(' · '.join(sorted(set(record['aliases']))))
                raw = raw.replace('data-pagefind-filter="bereich:wiki">', 'data-pagefind-filter="bereich:wiki"><span class="sw-visually-hidden" data-pagefind-weight="0.3">' + terms + '</span>', 1)
                target.write_text(raw, encoding='utf-8')
    searchable = [{k: r[k] for k in ("url", "title", "kind", "aliases")} for r in records
                  if not r["bridge_target"] and not r.get("duplicate_of") and r["source"] not in {"suche.md", "themen.md", "index.md", "neues.md"}]
    assets = site / "assets"
    assets.mkdir(exist_ok=True)
    (assets / "search-titles.json").write_text(json.dumps(searchable, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run([sys.executable, "-m", "pagefind", "--site", str(site)], capture_output=True, text=True)
    if result.returncode or not (site / "pagefind" / "pagefind.js").exists():
        raise RuntimeError("Pagefind index failed: " + result.stdout + result.stderr)
    (site / "build-info.json").write_text(json.dumps({**build, "search": "PASS", "indexed_pages": len(searchable), "deployment_verified": False}, indent=2), encoding="utf-8")
    if links['status'] != 'PASS':
        raise RuntimeError(f"Rendered internal links failed: {len(links['missing'])} missing targets; see site/rendered-links.json")
