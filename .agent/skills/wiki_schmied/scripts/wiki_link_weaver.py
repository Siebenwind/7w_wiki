import os
import re

WIKI_ROOT = "/Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki"

EXCLUDE_TITLES = ["index", "Die Archive", "Die Chronik"]

def get_wiki_map():
    wiki_map = {}
    for root, dirs, files in os.walk(WIKI_ROOT):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    title_match = re.search(r'title:\s*(.*)', content)
                    if title_match:
                        title = title_match.group(1).strip()
                        if title in EXCLUDE_TITLES:
                            continue
                        wiki_map[title] = os.path.splitext(file)[0]
    return wiki_map

def weave_links(filepath, wiki_map):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    sorted_titles = sorted(wiki_map.keys(), key=len, reverse=True)
    
    current_file_title = None
    title_match = re.search(r'title:\s*(.*)', content)
    if title_match:
        current_file_title = title_match.group(1).strip()

    processed_content = content
    for title in sorted_titles:
        if title == current_file_title:
            continue
        if len(title) < 3:
            continue
        
        # Regex to find title not inside [[ ]] or markdown links
        pattern = rf'(?<!\[\[)\b{re.escape(title)}\b(?!\]\])'
        processed_content = re.sub(pattern, f'[[{wiki_map[title]}]]', processed_content)

    if processed_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(processed_content)

def backlink_stories():
    stories_dirs = ["06_Erzählungen", "05_Geschichte"]
    for s_dir in stories_dirs:
        full_s_dir = os.path.join(WIKI_ROOT, s_dir)
        if not os.path.exists(full_s_dir):
            continue
            
        for file in os.listdir(full_s_dir):
            if file.endswith(".md"):
                filepath = os.path.join(full_s_dir, file)
                story_filename = os.path.splitext(file)[0]
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    story_title_match = re.search(r'title:\s*(.*)', content)
                    story_title = story_title_match.group(1).strip() if story_title_match else story_filename
                    
                    # Find all links
                    links = re.findall(r'\[\[(.*?)\]\]', content)
                    for link in set(links):
                        target_file = None
                        # Search for the file corresponding to the link
                        for root, dirs, files in os.walk(WIKI_ROOT):
                            if f"{link}.md" in files:
                                target_file = os.path.join(root, f"{link}.md")
                                break
                        
                        if target_file and ("07_Persoenlichkeiten" in target_file or "02_Geografie" in target_file):
                            add_backlink(target_file, story_title, story_filename)

def add_backlink(filepath, story_title, story_filename):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    content = "".join(lines)
    backlink_entry = f"- [[{story_filename}]]: Erwähnung in der Überlieferung."
    
    if f"[[{story_filename}]]" in content:
        return # Already linked
        
    # Find or create section
    section_header = "## Überlieferungen\n"
    if "## Überlieferungen" in content:
        # Append to existing section
        for i, line in enumerate(lines):
            if "## Überlieferungen" in line:
                lines.insert(i + 1, f"{backlink_entry}\n")
                break
    else:
        # Create at bottom, before Sources
        source_idx = -1
        for i, line in enumerate(lines):
            if "## Quellen" in line:
                source_idx = i
                break
        
        new_section = [f"\n{section_header}", f"{backlink_entry}\n"]
        if source_idx != -1:
            for j, s_line in enumerate(new_section):
                lines.insert(source_idx + j, s_line)
        else:
            lines.append("\n" + section_header + backlink_entry + "\n")
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)

if __name__ == "__main__":
    m = get_wiki_map()
    print(f"Mapped {len(m)} wiki titles.")
    for root, dirs, files in os.walk(WIKI_ROOT):
        for file in files:
            if file.endswith(".md"):
                weave_links(os.path.join(root, file), m)
    
    print("Backlinking stories...")
    backlink_stories()
