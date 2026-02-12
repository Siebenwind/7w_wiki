import os
import re
import sys

# Directory to Tag Mapping
TAG_MAPPING = {
    "00_Fundament": "#canon",
    "01_Pantheon": "#canon",
    "02_Geografie": "#canon",
    "03_Gesellschaft": "#canon",
    "04_Chronik": "#bote",
    "05_Geschichte": "#canon",
    "06_Erzählungen": "#perspektive",
    "07_Persoenlichkeiten": "#perspektive"
}

# Directory to Category Mapping
CATEGORY_MAPPING = {
    "00_Fundament": "Fundament",
    "01_Pantheon": "Religion",
    "02_Geografie": "Geografie",
    "03_Gesellschaft": "Gesellschaft",
    "04_Chronik": "Chronik",
    "05_Geschichte": "Geschichte",
    "06_Erzählungen": "Erzählung",
    "07_Persoenlichkeiten": "Persönlichkeit"
}

def sanitize_file(filepath):
    dirname = os.path.basename(os.path.dirname(filepath))
    default_tag = TAG_MAPPING.get(dirname, "#perspektive")
    default_cat = CATEGORY_MAPPING.get(dirname, "Sonstiges")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    content = "".join(lines)
    header_end_idx = -1
    
    # 1. Handle Frontmatter
    if not content.startswith('---'):
        # Insert default frontmatter if missing entirely
        filename_title = os.path.splitext(os.path.basename(filepath))[0].replace('_', ' ')
        frontmatter = [
            '---\n',
            'layout: wiki_page\n',
            f'title: {filename_title}\n',
            f'category: {default_cat}\n',
            '---\n\n'
        ]
        lines = frontmatter + lines
    else:
        # Frontmatter exists, check fields
        try:
            for i, line in enumerate(lines):
                if i > 0 and line.startswith('---'):
                    header_end_idx = i
                    break
            
            fm_lines = lines[1:header_end_idx]
            
            # Check layout
            if not any('layout: wiki_page' in l for l in fm_lines):
                # Replace layout if wrong or add if missing
                has_layout = False
                for j, l in enumerate(lines):
                    if 'layout:' in l:
                        lines[j] = 'layout: wiki_page\n'
                        has_layout = True
                if not has_layout:
                    lines.insert(1, 'layout: wiki_page\n')
                    header_end_idx += 1
            
            # Extract title for H1 comparison later
            title = "Unknown"
            for l in fm_lines:
                if l.startswith('title:'):
                    title = l.split(':', 1)[1].strip()
        except Exception as e:
            print(f"Error parsing frontmatter in {filepath}: {e}")

    # 2. Extract title from frontmatter for synchronization
    fm_content = "".join(lines)
    title_match = re.search(r'title:\s*(.*)', fm_content)
    title = title_match.group(1).strip() if title_match else "Unknown"

    # 3. Handle H1 and Epistemic Status
    h1_idx = -1
    for i, line in enumerate(lines):
        if line.startswith('# '):
            h1_idx = i
            h1_text = line[2:].strip()
            if h1_text != title:
                print(f"[FIX] Aligning H1 '{h1_text}' -> '{title}' in {filepath}")
                lines[i] = f"# {title}\n"
            break
    
    if h1_idx != -1:
        # Check if "Epistemischer Status" exists right after H1
        next_idx = h1_idx + 1
        # Skip empty lines
        while next_idx < len(lines) and lines[next_idx].strip() == "":
            next_idx += 1
        
        has_status = False
        if next_idx < len(lines):
            if "**Epistemischer Status:**" in lines[next_idx] or "Epistemischer Status:" in lines[next_idx]:
                has_status = True
            elif lines[next_idx].startswith("**Titel:**") or lines[next_idx].startswith("**Status:**"):
                 # Check next few lines for status
                 for k in range(next_idx, min(next_idx + 5, len(lines))):
                     if "Epistemischer Status:" in lines[k]:
                         has_status = True
                         break
        
        if not has_status:
            print(f"[FIX] Adding Status {default_tag} to {filepath}")
            lines.insert(h1_idx + 1, f"\n**Epistemischer Status:** {default_tag}\n")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".md"):
                sanitize_file(os.path.join(root, file))
