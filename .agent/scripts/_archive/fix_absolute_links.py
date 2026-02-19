import os
import re

ROOT_DIR = "/Users/alexandrerabe/siebenwind/7w_wiki"
WIKI_DIR = os.path.join(ROOT_DIR, "Siebenwind_Wiki")

def fix_links():
    link_pattern = re.compile(r'\[([^\]]+)\]\((file://[^)]+)\)')
    
    for root, dirs, files in os.walk(WIKI_DIR):
        for file in files:
            if not file.endswith(".md"):
                continue
                
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            new_content = content
            matches = link_pattern.findall(content)
            
            if not matches:
                continue
                
            print(f"Processing {file}...")
            
            for text, url in matches:
                # Handle file:///Quellen/...
                if url.startswith("file:///Quellen"):
                    # Assuming /Quellen maps to ROOT_DIR/Quellen
                    # Remove file://
                    path_part = url.replace("file://", "")
                    # Construct absolute path to target
                    abs_target = os.path.join(ROOT_DIR, path_part.lstrip("/"))
                    
                    # Calculate relative path from current file to target
                    try:
                        rel_path = os.path.relpath(abs_target, os.path.dirname(file_path))
                        # URL encode spaces? Markdown links usually handle spaces if encoded or wrapped in <>, but standard requests %20.
                        # Existing links likely have %20.
                        # url in regex usually captures what's there.
                        # If the original url had %20, we need to be careful.
                        # But standard os.path.relpath returns spaces.
                        rel_path_encoded = rel_path.replace(" ", "%20")
                        
                        replacement = f"[{text}]({rel_path_encoded})"
                        new_content = new_content.replace(f"[{text}]({url})", replacement)
                        print(f"  Fixed Source Link: {url} -> {rel_path_encoded}")
                    except ValueError:
                        print(f"  Could not calculate relpath for {url}")

                # Handle file:///Users/... (Absolute paths)
                elif url.startswith("file:///Users/"):
                    clean_path = url.replace("file://", "")
                    
                    # Case A: Points to Siebenwind_Wiki -> WikiLink
                    if clean_path.endswith(".md") and "Siebenwind_Wiki" in clean_path:
                         basename = os.path.basename(clean_path)
                         no_ext = os.path.splitext(basename)[0]
                         replacement = f"[[{no_ext}]]"
                         new_content = new_content.replace(f"[{text}]({url})", replacement)
                         print(f"  Converted to WikiLink: {url} -> {replacement}")
                    
                    # Case B: Points to Fuentes/Quellen -> Relative Link
                    elif "Quellen" in clean_path:
                        try:
                            rel_path = os.path.relpath(clean_path, os.path.dirname(file_path))
                            rel_path_encoded = rel_path.replace(" ", "%20")
                            replacement = f"[{text}]({rel_path_encoded})"
                            new_content = new_content.replace(f"[{text}]({url})", replacement)
                            print(f"  Fixed Absolute Source Link: {url} -> {rel_path_encoded}")
                        except ValueError:
                            print(f"  Could not calculate relpath for {url}")
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

if __name__ == "__main__":
    fix_links()
