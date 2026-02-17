import re
import os

def refactor_changelog(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Split into title and sections
    # Title is usually # Changelog or similar
    title_match = re.match(r'^# .*\n*', content)
    title = title_match.group(0).strip() if title_match else "# Changelog"
    
    # Extract sections starting with ##
    # Using a lookahead to keep the delimiters
    raw_sections = re.split(r'\n(?=## )', content[len(title):].strip())
    
    sections = []
    for rs in raw_sections:
        if not rs.strip().startswith("##"): continue
        lines = rs.strip().split('\n')
        header = lines[0].replace('## ', '').strip()
        body = '\n'.join(lines[1:]).strip()
        
        # Extract version/date for sorting: [2026-02-15.30]
        # We'll use the whole bracketed string as a sort key
        sort_key = ""
        key_match = re.search(r'\[(.*?)\]', header)
        if key_match:
            sort_key = key_match.group(1)
            
        sections.append({
            'header': header,
            'body': body,
            'sort_key': sort_key
        })

    # Sort reverse chronological (newest first)
    # Standard strings like 2026-02-15.30 sort well
    sections.sort(key=lambda x: x['sort_key'], reverse=True)

    output = [title]
    for i, s in enumerate(sections):
        is_open = " open" if i < 2 else ""
        output.append(f'<details{is_open}>\n<summary><b>{s["header"]}</b></summary>\n\n{s["body"]}\n</details>')

    with open(filepath + ".refactored", 'w') as f:
        f.write('\n\n'.join(output) + "\n\n---\n*Archivar: Antigravity*")

if __name__ == "__main__":
    refactor_changelog("CHANGELOG.md")
