import os
import re
import subprocess
from pathlib import Path

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
            
    return metadata, issues

def fix_file(filepath):
    try:
        content = Path(filepath).read_text(encoding="utf-8")
    except Exception as e:
        print(f"Lese-Fehler {filepath}: {e}")
        return

    metadata, fm_issues = check_frontmatter(content)
    new_content = content

    h1_match = re.search(r"^#\s+(.*)$", content, re.MULTILINE)
    if h1_match:
        h1_real = h1_match.group(1).strip()
        h1_clean = h1_real.replace('[[', '').replace(']]', '').replace('"', '').replace("'", "")
        
        # Determine replacing logic
        if metadata and "title" in metadata:
           title_norm = metadata["title"].strip('"').strip("'")
           if title_norm != h1_real:
                # Need to update the title in the frontmatter to exact H1
                # But we should wrap it in quotes if it contains special chars, or just generally wrap in quotes.
                
                # Careful replacement of the title line
                new_title_line = f"title: '{h1_real}'"
                new_content = re.sub(r'^title:\s*.*$', new_title_line, new_content, flags=re.MULTILINE)
        else:
           # Missing frontmatter or title entirely
           pass

    if new_content != content:
        try:
             Path(filepath).write_text(new_content, encoding='utf-8')
             print(f"Fixed title in: {filepath}")
        except Exception as e:
             print(f"Schreib-Fehler {filepath}: {e}")

# Find problematic files using the check output
print("Running ./7w_wiki.py check to find issues...")
result = subprocess.run(['./7w_wiki.py', 'check'], capture_output=True, text=True)
files_to_fix = set()

for line in result.stdout.split('\n'):
    if line.startswith('Siebenwind_Wiki/') and line.endswith(':'):
        files_to_fix.add(line[:-1])

print(f"Gefundene Dateien mit Fehlern: {len(files_to_fix)}")

for file in files_to_fix:
    fix_file(file)

print(f"Fertig.")
