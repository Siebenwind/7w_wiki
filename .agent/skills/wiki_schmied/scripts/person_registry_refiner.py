import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REGISTRY_FILE = REPO_ROOT / "docs" / "Siebenwind_Wiki" / "00_Fundament" / "Personenregister.md"

def refine_registry():
    with REGISTRY_FILE.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    
    header = lines[:13] # Keep frontmatter and table header
    data_lines = lines[13:]
    
    # Extract entries
    entries = []
    for line in data_lines:
        if "|" in line and "---" not in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 6:
                entries.append(parts[1:6]) # Name, Role, Source, Status, Link

    # Deduplicate and sort
    seen = set()
    unique_entries = []
    for e in entries:
        name = e[0]
        if name and name not in seen:
            unique_entries.append(e)
            seen.add(name)
    
    unique_entries.sort(key=lambda x: x[0]) # Sort by name

    # Reconstruct file
    new_content = "".join(header)
    for e in unique_entries:
        new_content += f"| {' | '.join(e)} |\n"
    
    with REGISTRY_FILE.open("w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"Refined Person Registry: {len(unique_entries)} unique entries sorted.")

if __name__ == "__main__":
    refine_registry()
