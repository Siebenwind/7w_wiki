import os
import re

WIKI_PATH = "/Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki"
GLOSSARY_FILE = "/Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki/00_Fundament/Glossar.md"

def build_glossary():
    terms = {}
    
    # Simple heuristic: capitalized words mentioned frequently
    # Excluding common German stop words and names in the Person Registry would be better
    term_pattern = r"\b([A-Z][a-zäöüß]+)\b"
    
    for root, _, files in os.walk(WIKI_PATH):
        for f in files:
            if f.endswith(".md") and f != "Glossar.md":
                with open(os.path.join(root, f), "r") as file:
                    content = file.read()
                    matches = re.findall(term_pattern, content)
                    for m in matches:
                        if len(m) > 3:
                            terms[m] = terms.get(m, 0) + 1

    # Filter terms mentioned more than 5 times
    relevant_terms = sorted([t for t, count in terms.items() if count > 5])

    # Write to Glossary file
    with open(GLOSSARY_FILE, "w") as f:
        f.write("---\nlayout: wiki_page\ntitle: Glossar\ncategory: Fundament\n---\n\n# Glossar\n\nDieses Glossar enthält wichtige Begriffe der Welt Siebenwind.\n\n| Begriff | Beschreibung | Status |\n|---------|--------------|--------|\n")
        for t in relevant_terms:
            f.write(f"| {t} | [DEFINITION_BENÖTIGT] | #canon |\n")
    
    print(f"Glossary built with {len(relevant_terms)} relevant terms.")

if __name__ == "__main__":
    build_glossary()
