import urllib.request
import re
import json
import time

def scan_forum(forum_id, max_pages=3):
    base_url = f"http://schnellerwind.mind.de/Foren/phpBB3/viewforum.php?f={forum_id}"
    topics = []
    
    # Updated regex: title and href can be in any order
    # Using a more permissive pattern to match the <a> tag
    topic_pattern = re.compile(r'<a [^>]*class="topictitle"[^>]*>([^<]+)</a>', re.DOTALL)
    attr_pattern = re.compile(r'(\w+)="([^"]+)"')
    
    for page in range(max_pages):
        start = page * 40
        url = f"{base_url}&start={start}"
        print(f"Scanning page {page+1} (start={start})...")
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                html = response.read().decode('utf-8', 'ignore')
                
                # Find all <a> tags with class="topictitle"
                for match in topic_pattern.finditer(html):
                    title = match.group(1).strip()
                    full_tag = match.group(0)
                    
                    # Extract attributes
                    attrs = dict(attr_pattern.findall(full_tag))
                    
                    href = attrs.get('href', '')
                    raw_date = attrs.get('title', '')
                    
                    # Extract topic ID from href
                    topic_id_match = re.search(r't=(\d+)', href)
                    topic_id = topic_id_match.group(1) if topic_id_match else "unknown"
                    
                    # Clean up date
                    clean_date = raw_date.replace('Verfasst: ', '')
                    
                    topics.append({
                        "id": topic_id,
                        "title": title,
                        "date": clean_date,
                        "url": f"http://schnellerwind.mind.de/Foren/phpBB3/viewtopic.php?f={forum_id}&t={topic_id}"
                    })
            
            time.sleep(0.5) 
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break
            
    return topics

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Siebenwind Forum Scanner")
    parser.add_argument("--forum_id", type=int, default=6, help="Forum ID (6=Bekanntmachungen, 1=News)")
    parser.add_argument("--pages", type=int, default=3, help="Number of pages to scan")
    parser.add_argument("--output", default="forum_scan_results.json", help="Output JSON file")
    
    args = parser.parse_args()
    
    results = scan_forum(args.forum_id, max_pages=args.pages)
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        
    print(f"Done. Extracted {len(results)} topics to {args.output}.")
