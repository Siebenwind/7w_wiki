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
    
    return all_issues

def main():
    parser = argparse.ArgumentParser(description="Siebenwind Lektor - Style Checker")
    parser.add_argument("path", help="Datei oder Verzeichnis zum Prüfen")
    args = parser.parse_args()
    
    target = Path(args.path)
    if not target.exists():
        print(f"{RED}Pfad nicht gefunden:{RESET} {target}")
        sys.exit(1)
        
    files = [target] if target.is_file() else target.rglob("*.md")
    
    error_count = 0
    file_count = 0
    
    print(f"Prüfe {target}...\n")
    
    for file_path in files:
        file_count += 1
        issues = check_file(file_path)
        if issues:
            error_count += 1
            print(f"{os.path.relpath(file_path, start=os.getcwd())}:")
            for issue in issues:
                print(f"  - {issue}")
            print("")
            
    if error_count == 0:
        print(f"{GREEN}Alles sauber!{RESET} ({file_count} Dateien geprüft)")
    else:
        print(f"{RED}{error_count} Dateien mit Problemen gefunden.{RESET} ({file_count} gesamt)")
        sys.exit(1)

if __name__ == "__main__":
    main()
