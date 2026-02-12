import os
import re

WIKI_PATH = "/Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki"
TIMELINE_FILE = "/Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki/05_Geschichte/Zeitstrahl.md"

def weave_timeline():
    events = []
    
    # Regex for years like "122 n.H." or "Sonnenzirkel 42"
    year_pattern = r"(\d{1,4}\s*n\.H\.)"
    
    for root, _, files in os.walk(WIKI_PATH):
        for f in files:
            if f.endswith(".md") and f != "Zeitstrahl.md":
                page_name = f.replace(".md", "")
                with open(os.path.join(root, f), "r") as file:
                    content = file.read()
                    matches = re.findall(year_pattern, content)
                    for m in matches:
                        # Extract context (sentence around the year)
                        sentence_match = re.search(r"([^.?!]*" + re.escape(m) + r"[^.?!]*[.?!])", content)
                        context = sentence_match.group(0).strip() if sentence_match else "Ereignis erwähnt."
                        events.append({"year": m, "source": page_name, "context": context})

    # Sort events (basic string sort for now, needs numeric sorting for production)
    events.sort(key=lambda x: x['year'])

    # Write to Timeline file
    with open(TIMELINE_FILE, "w") as f:
        f.write("---\nlayout: wiki_page\ntitle: Zeitstrahl\ncategory: Geschichte\n---\n\n# Zeitstrahl\n\n| Jahr | Ereignis / Kontext | Quelle |\n|------|---------------------|--------|\n")
        for e in events:
            f.write(f"| {e['year']} | {e['context']} | [[{e['source']}]] |\n")
    
    print(f"Timeline woven with {len(events)} historical data points.")

if __name__ == "__main__":
    weave_timeline()
