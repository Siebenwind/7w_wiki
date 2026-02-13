import os
import re

# Paths
PERSONEN_DIR = "/Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki/07_Persoenlichkeiten"
REGISTER_FILE = "/Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki/00_Fundament/Personenregister.md"

def find_orphans():
    # 1. Get List of Files (strip extension)
    files = [f.replace('.md', '') for f in os.listdir(PERSONEN_DIR) if f.endswith('.md')]
    print(f"Found {len(files)} profiles in directory.")

    # 2. Extract Links from Register
    with open(REGISTER_FILE, 'r') as f:
        content = f.read()
    
    # Regex for [[Wikilinks]]
    registered_names = set(re.findall(r'\[\[(.*?)\]\]', content))
    
    # Handle piped links like [[Target|Label]] - we need 'Target'
    cleaned_registered_names = set()
    for name in registered_names:
        if '|' in name:
            cleaned_registered_names.add(name.split('|')[0])
        else:
            cleaned_registered_names.add(name)
            
    # 3. Compare
    orphans = []
    for person in files:
        if person not in cleaned_registered_names:
            orphans.append(person)
            
    # 4. specialized checks (sometimes filenames differ slightly from register names)
    # This simple check assumes exact match.
    
    print(f"Found {len(orphans)} orphans:")
    for orphan in sorted(orphans):
        print(f"- {orphan}")

if __name__ == "__main__":
    find_orphans()
