import os
import shutil
import re
import json
import argparse
from pathlib import Path

# Paths
BASE_DIR = Path("/Users/alexandrerabe/siebenwind/7w_wiki")
QUELLEN_DIR = BASE_DIR / "Quellen"
TEMP_MD_DIR = QUELLEN_DIR / "TEMP_MARKDOWN_QUELLEN"
ARCHIV_DIR = QUELLEN_DIR / "_ARCHIV_ORIGINAL"

def normalize_name(name):
    """Normalize file name for matching: lowercase, alphanumeric, remove common debris."""
    name = name.lower()
    # Remove extensions
    name = Path(name).stem
    # Remove common pipe/web debris
    name = re.sub(r'\s*\|\s*siebenwind\s*\|\s*ultima\s*online\s*freeshard\s*\|\s*siebenwind', '', name)
    # Remove special chars
    name = re.sub(r'[^a-zA-Z0-9]', '', name)
    return name

def build_original_map():
    """Build a map of normalized names to original file paths."""
    original_map = {}
    for folder in ["Hintergrund", "Bibliothek Astrael", "Bibliothek Toran Dur", "Zeitung 7w Bote", "Spielergeschichten"]:
        dir_path = QUELLEN_DIR / folder
        if not dir_path.exists():
            continue
        for file in dir_path.rglob("*"):
            if file.is_file() and not file.name.startswith(".") and file.suffix != ".md":
                normalized = normalize_name(file.name)
                if normalized not in original_map:
                    original_map[normalized] = []
                original_map[normalized].append(file)
    return original_map

def is_good_markdown(content):
    """Heuristic check for markdown quality."""
    # Check for excessive HTML tags (indicates failed conversion)
    # A full HTML page usually has > 100 tags. A few <mailto> or escaped chars are fine.
    html_tags = len(re.findall(r'<[a-z/][^>]*>', content, re.IGNORECASE))
    if html_tags > 50: 
        return False
        
    # Check for markdown indicators: Headers, Bold, Horizontal Rules, or Lists
    has_headers = re.search(r'^#+\s+', content, re.MULTILINE)
    has_bold = re.search(r'\*\*.*?\*\*', content)
    has_hr = re.search(r'^---+\s*$', content, re.MULTILINE)
    has_lists = re.search(r'^\s*[\*\-\+]\s+', content, re.MULTILINE) or re.search(r'^\s*\d+\.\s+', content, re.MULTILINE)
    
    # If it has at least one indicator
    if has_headers or has_bold or has_hr or has_lists:
        return True
    
    # If it's a long plain text file (likely a dictionary or essay), and has very few HTML tags, it's "good enough"
    if len(content) > 500 and html_tags < 5:
        return True

    return False

def run_integration(dry_run=True):
    original_map = build_original_map()
    stats = {"integrated": 0, "mismatched": 0, "low_quality": 0, "errors": 0}
    log = []

    if not TEMP_MD_DIR.exists():
        print(f"Error: {TEMP_MD_DIR} does not exist.")
        return

    for md_file in TEMP_MD_DIR.glob("*.md"):
        norm_name = normalize_name(md_file.name)
        
        matches = original_map.get(norm_name, [])
        
        if not matches:
            stats["mismatched"] += 1
            log.append({"file": md_file.name, "status": "mismatched", "reason": "No original file found with similar name"})
            continue
        
        if len(matches) > 1:
            stats["errors"] += 1
            log.append({"file": md_file.name, "status": "error", "reason": f"Multiple matches found: {[m.name for m in matches]}"})
            continue
            
        original_file = matches[0]
        
        # Read content for quality check
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try latin-1 if utf-8 fails (sometimes conversion artifacts)
            try:
                with open(md_file, "r", encoding="latin-1") as f:
                    content = f.read()
            except Exception as e:
                stats["errors"] += 1
                log.append({"file": md_file.name, "status": "error", "reason": f"Read error: {str(e)}"})
                continue

        if not is_good_markdown(content):
            stats["low_quality"] += 1
            log.append({"file": md_file.name, "status": "low_quality", "reason": "Heuristic quality check failed"})
            continue

        # Integration Logic
        target_md_path = original_file.parent / (original_file.stem + ".md")
        archiv_target_path = ARCHIV_DIR / original_file.relative_to(QUELLEN_DIR)

        if dry_run:
            log.append({"file": md_file.name, "status": "dry_run", "target": str(target_md_path), "original_archived_to": str(archiv_target_path)})
            stats["integrated"] += 1
        else:
            try:
                # 1. Create Archive Directory
                archiv_target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 2. Move Original to Archive
                shutil.move(str(original_file), str(archiv_target_path))
                
                # 3. Move/Write MD to Target
                # We write it to ensure UTF-8 and clean up any potential latin-1 artifacts
                with open(target_md_path, "w", encoding="utf-8") as f:
                    f.write(content)
                
                # 4. Remove original md from TEMP (after successful write)
                # md_file.unlink() # Maybe don't delete yet for safety?
                
                log.append({"file": md_file.name, "status": "integrated", "target": str(target_md_path)})
                stats["integrated"] += 1
            except Exception as e:
                stats["errors"] += 1
                log.append({"file": md_file.name, "status": "error", "reason": f"Operation error: {str(e)}"})

    # Print Report
    print(json.dumps(stats, indent=2))
    log_file = BASE_DIR / "Logs" / "integration_report.json"
    log_file.parent.mkdir(exist_ok=True)
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)
    print(f"Detailed log written to {log_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Integrate Markdown conversions.")
    parser.add_argument("--run", action="store_true", help="Perform actual file operations.")
    args = parser.parse_args()
    
    run_integration(dry_run=not args.run)
