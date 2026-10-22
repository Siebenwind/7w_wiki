"""Reader and operator projections, invoked by the canonical stats command."""
import html
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"


def title_of(path):
    raw = path.read_text(encoding="utf-8")
    match = re.search(r"^# (.+)$", raw, re.MULTILINE)
    title = match.group(1) if match else path.stem
    title = re.sub(r"\[\[(?:[^]|]+\|)?([^]]+)\]\]", r"\1", title)
    return title.replace("_", " ").replace("[", "").replace("]", "").strip()


def load_updates():
    payload = json.loads((ROOT / ".agent/data/reader_updates.json").read_text(encoding="utf-8"))
    rows = []
    for row in payload["updates"]:
        date.fromisoformat(row["date"])
        if row["status"] not in {"draft", "published"}:
            raise ValueError("Unknown reader publication status")
        if not row["title"] or not row["summary"] or not row["articles"]:
            raise ValueError("Reader update must have title, summary and articles")
        for article in row["articles"]:
            target = (DOCS / article).resolve()
            if not target.is_relative_to(DOCS.resolve()) or not target.is_file():
                raise ValueError("Missing reader update article: " + article)
        if row["status"] == "published" and date.fromisoformat(row["date"]) <= date.today():
            rows.append(row)
    return sorted(rows, key=lambda r:r["date"], reverse=True)


def activity_html(rows):
    cards = []
    for row in rows[:3]:
        article = row["articles"][0]
        url = quote(article[:-8] if article.endswith('index.md') else article[:-3] + '/', safe='/')
        cards.append(f'<article class="activity-card"><p class="activity-meta">{row["date"]}</p><h3><a href="{url}">{html.escape(row["title"])}</a></h3><p>{html.escape(row["summary"])}</p></article>')
    return '<!-- BEGIN GENERATED PUBLIC ACTIVITY -->\n<div class="activity-grid">' + ''.join(cards) + '</div>\n<p><a href="neues/">Alle Neuigkeiten</a></p>\n<!-- END GENERATED PUBLIC ACTIVITY -->'


def sync_reader_catalog():
    sync_documentation_inventory()
    rows = load_updates()
    news = ["---", "title: Neues im Archiv", "---", "", "# Neues im Archiv", "", "Neue und erweiterte Artikel. Die Datumsangaben bezeichnen den dokumentierten Abschluss der Bearbeitung; sie sind keine Ereignisdaten der Spielwelt.", ""]
    for row in rows:
        news += [f'## {row["date"]}: {row["title"]}', "", row["summary"], ""]
        news += [f'- [{title_of(DOCS / p)}]({p})' for p in row["articles"]]
        news.append("")
    (DOCS / "neues.md").write_text('\n'.join(news), encoding="utf-8")
    topics = {}
    for path in sorted((DOCS / "Siebenwind_Wiki").rglob("*.md")):
        raw = path.read_text(encoding="utf-8")
        if path.name == "index.md" or re.search(r"^bridge_target:",raw,re.MULTILINE):
            continue
        title = title_of(path)
        initial = title[0].upper() if title else "#"
        if not initial.isalpha(): initial = "#"
        topics.setdefault(initial, []).append((title,path.relative_to(DOCS).as_posix()))
    az = ['---', 'title: Themen A–Z', '---', '', '# Themen A–Z', '', 'Ein alphabetischer Zugang zu den Wikiartikeln. Quellen und technische Berichte findest du über die Bereichsauswahl der Suche.', '']
    for initial,entries in sorted(topics.items()):
        az += ['## '+initial,'']
        az += [f'- [{t}]({quote(p,safe="/")})' for t,p in sorted(entries,key=lambda e:e[0].casefold())]
        az.append('')
    (DOCS / 'themen.md').write_text('\n'.join(az),encoding='utf-8')
    return rows


def sync_documentation_inventory():
    """Conservative inventory: an unreviewed runbook is never silently certified current."""
    reviewed = {'docs/setup_rag.md', 'docs/STYLING.md', 'System/STYLING.md', 'docs/architecture.md', 'docs/CONTRIBUTING.md', 'docs/Agenten/index.md', 'docs/Agenten/leserseiten.md', 'docs/Agenten/status.md', '.agent/prompts/Oberarchivar.md', '.agent/prompts/Archivar.md', 'docs/Archiv/QUALITAETSRAHMEN_2026.md', 'System/Synapse_Board/SY_TESTING.md'}
    reviewed.update({'docs/index.md', 'docs/forschung.md', 'docs/neues.md', 'docs/suche.md', 'docs/themen.md'})
    reviewed_october = {
        '.agent/prompts/Archivar.md', '.agent/prompts/Auskunfts_Archivar.md',
        '.agent/prompts/EXTERNAL_KICKOFF.md', '.agent/prompts/EXTERNAL_SCOUT_TASK.md',
        '.agent/prompts/HOMEPAGE_NEWS_TASK.md', 'System/AGENT_OPERATIONS_HANDBOOK.md',
        'System/COORDINATION_HUB.md', 'System/MCP/README.md', 'System/PRODUCTION_PROTOCOL.md',
        'System/Synapse_Board/CORE_LORE_SCORE_GUIDE.md', 'System/Synapse_Board/LORE_RESEARCH_BOARD.md',
        'System/Synapse_Board/SILICON_INQUISITION/MANIFEST.md', 'System/Synapse_Board/SY_BULLETIN.md',
        'System/Synapse_Board/SY_DISPATCH.md', 'System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md',
        'System/Synapse_Board/SY_HISTORIAN_TRACEABILITY.md', 'System/Synapse_Board/SY_INTEROP.md',
        'System/Synapse_Board/SY_REVIEW.md', 'System/Synapse_Board/SY_STANDARDS.md',
        'System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md', 'System/Synapse_Board/_TEMPLATE_AUDIT_REQUEST.md',
        'System/Synapse_Board/_TEMPLATE_RESEARCH.md', 'System/Synapse_Board/_TEMPLATE_TICKET.md',
        'System/Templates/HISTORIAN_CLOSEOUT_TEMPLATE.md', 'System/Templates/INGESTION_REPORT_TEMPLATE.md',
        'docs/AGENT_OPERATIONS_HANDBOOK.md', 'docs/Agenten/dispatch.md', 'docs/Agenten/interop.md',
        'docs/Agenten/workflows.md', 'docs/CHANGELOG.md', 'docs/COORDINATION_HUB.md',
        'docs/LICENSE.md', 'docs/MASTER_TASK_LIST.md',
    }
    reviewed_october.update('.agent/workflows/' + name + '.md' for name in (
        'antigravity', 'decide', 'delegate', 'forum_search', 'handover', 'herold', 'historian',
        'ingest_master', 'lore_master', 'meta_master', 'qa_master', 'scout', 'start',
        'takeover', 'tech_master', 'test_run', 'translate', 'wiki_style_guide'))
    reviewed.update(reviewed_october)
    historical_records = {
        '.agent/prompts/Kickoff.md',
        'System/Synapse_Board/SILICON_INQUISITION/INQ-2026-001_Astral_Web_Doubt.md',
        'System/Synapse_Board/SILICON_INQUISITION/INQ-2026-002_Canon_Audit_Desires.md',
    }
    paths=set()
    for folder in ['.agent/docs','.agent/prompts','.agent/workflows','System','docs/Agenten']:
        paths.update((ROOT/folder).rglob('*.md'))
    paths.update(DOCS.glob('*.md'))
    paths.update(DOCS/'Archiv'/name for name in ['QUALITAETSRAHMEN_2026.md','REDESIGN_ROADMAP_2026.md'])
    paths={p for p in paths if not any(part in {'DISPATCH','RESEARCH','Archivregister','Ingestion_Reports'} for part in p.relative_to(ROOT).parts) and not p.name.startswith(('RESEARCH-', 'Conflict_', 'Batch_'))}
    rows=[]
    for path in sorted(paths):
        name=path.relative_to(ROOT).as_posix()
        if name.endswith('DOCUMENTATION_INVENTORY.md') or path.name.startswith('READER_RELEASE_REVIEW_'): continue
        raw=path.read_text(encoding='utf-8')
        historical=name in historical_records or ('Templates' not in path.parts and any(t in name.lower() for t in ['archive','dossier','roadmap','report','evaluation','session_']))
        state='aktuell' if name in reviewed else 'historisch' if historical else 'zu korrigieren'
        reason='Gegen Implementierung/CLI geprüft, 2026-09-12' if state=='aktuell' else 'Zeitgebundener Bericht; keine aktive Betriebsanleitung' if state=='historisch' else 'Aktive Anleitung/Referenz: fachlicher Abgleich noch erforderlich'
        if name in reviewed_october:
            reason='Technischer CLI-, Pfad- und Vertragsabgleich, 2026-10-21; keine fachliche Lorefreigabe'
        if re.search(r'\]\(file://',raw) and state!='aktuell': reason+='; lokale Datei-URLs'
        if re.search(r'(?<![\w/])/(?:antigravity|audit)\b',raw) and state!='aktuell': reason+='; alte Workflow-Kurzform'
        rows.append({'path':name,'status':state,'reason':reason})
    inventory={'date':date.today().isoformat(),'scope':'System (ohne Dispatch/Forschung/Archivregister), aktive Agent-Dokumentation, öffentliche Technik- und Wurzelseiten','entries':rows}
    (ROOT/'.agent/data/documentation_inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
    md=['# Dokumentationsinventar','',f'Stand: {inventory["date"]}. {inventory["scope"]}.','', '„Aktuell“ bedeutet einen dokumentierten Implementierungsabgleich. Ungeprüfte Anleitungen bleiben ausdrücklich „zu korrigieren“. Historische Texte erhalten ihren ursprünglichen Inhalt; für laufenden Betrieb gilt `docs/Agenten/leserseiten.md` beziehungsweise das kanonische Betriebshandbuch. Keine Aussage zur fachlichen Aktualität sämtlicher Loreartikel.','', '| Datei | Einordnung | Nachweis / offener Abgleich |','| :--- | :--- | :--- |']
    md += [f'| `{r["path"]}` | {r["status"]} | {r["reason"]} |' for r in rows]
    (ROOT/'System/DOCUMENTATION_INVENTORY.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
