import os
import re

def check_links(directory):
    absolute_pattern = re.compile(r'file:///Users/[a-zA-Z0-9_/.]+')
    issues = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = absolute_pattern.findall(content)
                    if matches:
                        issues.append((path, matches))
                        
    return issues

if __name__ == "__main__":
    wiki_dir = "docs/Siebenwind_Wiki"
    found_issues = check_links(wiki_dir)
    
    if found_issues:
        print(f"⚠️ Found absolute links in {len(found_issues)} files:")
        for path, matches in found_issues:
            print(f"- {path}: {len(matches)} absolute links")
    else:
        print("✅ No absolute links found in Wiki.")
