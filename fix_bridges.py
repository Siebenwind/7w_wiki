import os
import re
from pathlib import Path

WIKI_DIR = Path("Siebenwind_Wiki")

def fix_bridges():
    count_fixed = 0
    for filepath in WIKI_DIR.rglob("*.md"):
        try:
            content = filepath.read_text(encoding="utf-8")
        except:
            continue
            
        # Is it a bridge file?
        if "Brueckenartikel zur Stabilisierung" in content or "status: UNGEKLAERT" in content:
            # Does it have missing bridge fields?
            if "bridge_mode:" not in content:
                # Add bridge metadata to frontmatter
                new_frontmatter = (
                    "bridge_mode: STUB\n"
                    "bridge_target: TBD\n"
                    "bridge_ticket: NONE\n"
                    "bridge_review_until: 2026-12-31\n"
                    "---"
                )
                
                # Replace closing --- of frontmatter
                parts = content.split("---\n", 2)
                if len(parts) >= 3:
                    parts[1] = parts[1] + new_frontmatter + "\n"
                    new_content = "---\n".join(parts[:-1]) + parts[-1] 
                else:
                    new_content = re.sub(r'---$', new_frontmatter, content, count=1, flags=re.MULTILINE)
                    
                filepath.write_text(new_content, encoding="utf-8")
                count_fixed += 1
                
    print(f"Bridges fixed: {count_fixed}")

if __name__ == "__main__":
    fix_bridges()
