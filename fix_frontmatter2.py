import os
import re
import subprocess

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Lese-Fehler {filepath}: {e}")
        return

    # Try to find H1
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    h1_title = h1_match.group(1).strip() if h1_match else None
    
    clean_title = None
    if h1_title:
        # Clean H1 for frontmatter title
        clean_title = h1_title.replace('[[', '').replace(']]', '')

    new_content = content
    if h1_title:
        # Fix title mismatch directly in frontmatter
        new_content = re.sub(r'^title:\s*.*$', f"title: '{clean_title}'", new_content, flags=re.MULTILINE)

    if new_content != content:
        try:
             with open(filepath, 'w', encoding='utf-8') as f:
                 f.write(new_content)
             print(f"Fixed: {filepath}")
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
