#!/usr/bin/env python3
import os
import sys
import re
import json
import argparse
from pathlib import Path

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def strip_ansi(text: str) -> str:
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

APP_DIR = Path(__file__).parent
CONFIG_FILE = APP_DIR / "style_guide.json"

def load_config():
    if not CONFIG_FILE.exists():
        print(f"{RED}Fehler: Konfigurationsdatei nicht gefunden: {CONFIG_FILE}{RESET}")
        sys.exit(1)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

CONFIG = load_config()

def check_frontmatter(content):
    issues = []
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        issues.append("Kein YAML Frontmatter gefunden.")
        return None, issues
    
    fm_text = match.group(1)
    metadata = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            metadata[key.strip()] = val.strip()
            
    for req in CONFIG.get("required_frontmatter", []):
        if req not in metadata:
            issues.append(f"Fehlendes Frontmatter-Feld: '{req}'")
            
    return metadata, issues

def check_style(content):
    issues = []
    
    # Remove Frontmatter and Code Blocks for text analysis
    text = re.sub(r"^---\n.*?\n---", "", content, flags=re.DOTALL)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    
    # Check No-Go Words
    for word in CONFIG.get("no_go_words", []):
        if re.search(r"\b" + re.escape(word) + r"\b", text, re.IGNORECASE):
            issues.append(f"{RED}Verbotener Begriff:{RESET} '{word}' gefunden.")
            
    # Check Preferred Terms
    for bad, good in CONFIG.get("preferred_terms", {}).items():
        if re.search(r"\b" + re.escape(bad) + r"\b", text, re.IGNORECASE):
            issues.append(f"{YELLOW}Vorschlag:{RESET} Nutze '{good}' statt '{bad}'.")
            
    # Check Passive Voice (Simple Heuristic: 'wurden', 'werden')
    passive_markers = ["wurde", "wurden", "worden", "wird"]
    found_passive = [w for w in passive_markers if re.search(r"\b" + w + r"\b", text, re.IGNORECASE)]
    if len(found_passive) > 5: # Threshold
         issues.append(f"{BLUE}Stil:{RESET} Hohe Dichte an Passiv-Konstruktionen ({len(found_passive)} Marker gefunden).")
         
    return issues

def check_forum_article_tone(content, metadata):
    issues = []
    if not metadata:
        return issues

    epistemic = metadata.get("epistemic", "")
    source = metadata.get("quelle", "") or metadata.get("source", "")
    is_forum_article = "#forum" in epistemic or "Quellen/Forum" in source
    if not is_forum_article:
        return issues

    # References may name raw archival assets; the article body should not read like an ingest report.
    text = re.sub(r"^---\n.*?\n---", "", content, flags=re.DOTALL)
    main_body = re.split(r"^##\s+Referenzen\s*$", text, maxsplit=1, flags=re.MULTILINE)[0]
    forbidden = [
        (r"archivierte Forumquelle", "Forum-Archivstatus gehoert in Frontmatter, Referenzen oder Report, nicht in den Artikelkoerper."),
        (r"nicht automatisch kanonisiert", "Kanonisierungs-Boilerplate gehoert in Metadaten oder Report, nicht in den Artikelkoerper."),
        (r"Raw HTML", "Raw-HTML-Hinweise gehoeren nur in Referenzen oder Report."),
        (r"Registerstatus|Registerlogik", "Registerhinweise gehoeren nicht in den Artikelkoerper."),
        (r"Die Quelle bleibt", "Quellenkarten-Formulierung statt Wiki-Ton."),
        (r"Die Aussagen dieser Seite bleiben", "Quellenkarten-Formulierung statt Wiki-Ton."),
        (r"^##\s+Einordnung\s*$", "Generische Einordnung ist fuer Forum-Neuanlagen kein Produktionsstandard."),
        (r"!!! info \"Metadaten\"[\s\S]{0,220}Forumquelle", "Sichtbare technische Forum-Metabox statt Wiki-Ton."),
    ]
    for pattern, message in forbidden:
        if re.search(pattern, main_body, re.IGNORECASE | re.MULTILINE):
            issues.append(f"{YELLOW}Forum-Ton:{RESET} {message}")

    return issues

def check_file(path):
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"Fehler beim Lesen: {e}"]
        
    all_issues = []
    
    # 1. Frontmatter Check
    metadata, fm_issues = check_frontmatter(content)
    all_issues.extend(fm_issues)
    
    # 2. H1 Check (if title exists)
    if metadata and "title" in metadata:
        title_norm = metadata["title"].strip('"').strip("'")
        h1_match = re.search(r"^#\s+(.*)$", content, re.MULTILINE)
        if not h1_match:
            all_issues.append("Keine H1-Überschrift gefunden.")
        elif h1_match.group(1).strip() != title_norm:
            all_issues.append(f"Titel-Mismatch: H1='{h1_match.group(1).strip()}' != Frontmatter='{title_norm}'")
            
    # 3. Style Check
    style_issues = check_style(content)
    all_issues.extend(style_issues)
    all_issues.extend(check_forum_article_tone(content, metadata))
    
    return all_issues

def main():
    parser = argparse.ArgumentParser(description="Siebenwind Lektor - Style Checker")
    parser.add_argument("path", help="Datei oder Verzeichnis zum Prüfen")
    parser.add_argument("--json", action="store_true", help="Output raw JSON report (suppresses stdout)")
    args = parser.parse_args()
    
    target = Path(args.path)
    if not target.exists():
        if not args.json:
            print(f"{RED}Pfad nicht gefunden:{RESET} {target}")
        sys.exit(1)
        
    files = [target] if target.is_file() else list(target.rglob("*.md"))
    
    error_count = 0
    file_count = 0
    issues_dict = {}
    
    if not args.json:
        print(f"Prüfe {target}...\n")
    
    for file_path in files:
        file_count += 1
        issues = check_file(file_path)
        if issues:
            error_count += 1
            rel_path = os.path.relpath(file_path, start=os.getcwd())
            issues_dict[rel_path] = [strip_ansi(i) for i in issues]
            
            if not args.json:
                print(f"{rel_path}:")
                for issue in issues:
                    print(f"  - {issue}")
                print("")
            
    if args.json:
        print(json.dumps({
            "files_checked": file_count,
            "files_with_issues": error_count,
            "issues": issues_dict
        }, indent=2))
        if error_count > 0:
            sys.exit(1)
        return
            
    if error_count == 0:
        print(f"{GREEN}Alles sauber!{RESET} ({file_count} Dateien geprüft)")
    else:
        print(f"{RED}{error_count} Dateien mit Problemen gefunden.{RESET} ({file_count} gesamt)")
        sys.exit(1)

if __name__ == "__main__":
    main()
