import argparse
import re
import os
import json

# Simplified titles (non-capturing for the alternation itself)
TITLES = [
    "König", "Königin", "Herzog", "Herzogin", "Fürst", "Fürstin", 
    "Graf", "Gräfin", "Baron", "Baronin", "Baronesse", "Komtesse", 
    "Junker", "Junkerin", "Ritter", "Freiherr", "Freiherrin", "Edler", "Edle",
    "Geweihter", "Geweihte", "Erzgeweihter", "Erzgeweihte", "Abt", "Äbtissin", 
    "Kaplan", "Bischof", "Priester", "Priesterin",
    "Kanzler", "Kanzlerin", "Patrizier", "Patrizierin", "Kregor", 
    "Vogt", "Vogtin", "Richter", "Richterin", "Häuptling", "Schatzkanzler", "Schatzkanzlerin"
]

TITLES_REGEX = r"(?:" + "|".join(TITLES) + r")"
NAME_REGEX = r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"
LINEAGE_REGEX = r"(?:\s+(?:ap|ahm)\s+([A-Z][a-z]+))?"
LOCAL_REGEX = r"(?:\s+(?:von|zu)\s+([A-Z][a-z]+(?:\-[A-Z][a-z]+)*))?"

pattern = re.compile(rf"\b({TITLES_REGEX})\s+{NAME_REGEX}{LINEAGE_REGEX}{LOCAL_REGEX}", re.IGNORECASE)

def extract_personas(file_path):
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

    results = []
    for m in pattern.finditer(content):
        results.append({
            "title": m.group(1),
            "name": m.group(2),
            "lineage": m.group(3),
            "location": m.group(4),
            "source": os.path.basename(file_path)
        })
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["extract"])
    parser.add_argument("--path", required=True)
    args = parser.parse_args()

    if args.command == "extract":
        if os.path.isfile(args.path):
            findings = extract_personas(args.path)
            print(json.dumps(findings, indent=2))
        elif os.path.isdir(args.path):
            all_findings = []
            for root, _, files in os.walk(args.path):
                for file in files:
                    if file.endswith((".html", ".md", ".txt")):
                        all_findings.extend(extract_personas(os.path.join(root, file)))
            
            # Deduplicate
            seen = set()
            unique = []
            for f in all_findings:
                key = (f["name"], f["title"])
                if key not in seen:
                    unique.append(f)
                    seen.add(key)
            print(json.dumps(unique, indent=2))

if __name__ == "__main__":
    main()
