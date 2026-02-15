import sys
from datetime import datetime
import re

def add_changelog_entry(topic, additions=None, changes=None, removals=None):
    filepath = "CHANGELOG.md"
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Read current content
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    # Find current version/index for the day
    # Pattern: [2026-02-15.30]
    pattern = rf"\[{date_str}\.(\d+)\]"
    max_idx = 0
    for line in lines:
        match = re.search(pattern, line)
        if match:
            max_idx = max(max_idx, int(match.group(1)))
    
    new_version = f"[{date_str}.{max_idx + 1}]"
    
    entry = [f'<details open>\n<summary><b>{new_version} - {topic}</b></summary>\n']
    
    if additions:
        entry.append("### Hinzugefügt\n")
        entry.extend([f"- {a}\n" for a in additions])
        entry.append("\n")
    if changes:
        entry.append("### Geändert\n")
        entry.extend([f"- {c}\n" for c in changes])
        entry.append("\n")
    if removals:
        entry.append("### Entfernt\n")
        entry.extend([f"- {r}\n" for r in removals])
        entry.append("\n")
        
    entry.append("</details>\n")
    
    # Insert after the title (# Changelog)
    # Find the line after # Changelog
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_pos = i + 1
            break
            
    # Remove 'open' from previous entries
    content = "".join(lines)
    content = content.replace("<details open>", "<details>")
    
    new_lines = content.splitlines(keepends=True)
    final_content = new_lines[:insert_pos] + ["\n"] + entry + ["\n"] + new_lines[insert_pos:]
    
    with open(filepath, 'w') as f:
        f.writelines(final_content)
    print(f"✅ Entry {new_version} added to {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python changelog_tool.py 'Topic' 'Additions...'")
    else:
        topic = sys.argv[1]
        additions = sys.argv[2:] if len(sys.argv) > 2 else []
        add_changelog_entry(topic, additions=additions)
