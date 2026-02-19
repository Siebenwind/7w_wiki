import os
import re
import sys

def parse_frontmatter_block(block: str) -> dict:
    meta = {}
    for line in block.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta

def calculate_initial_score(metadata):
    """Calculates entry score based on epistemic rank."""
    ranks = {
        '#user_canon': 10,
        '#canon': 8,
        '#bote': 5,
        '#überlieferung': 3,
        '#perspektive': 2
    }
    
    # Check multiple fields for epistemic tags
    epistemic_tag = '#perspektive'
    for key in ['epistemic', 'status', 'tags']:
        if key in metadata and metadata[key].startswith('#'):
            epistemic_tag = metadata[key]
            break

    score = ranks.get(epistemic_tag, 1)
    
    # Bonuses
    if metadata.get('quelle') and 'Hintergrund' in metadata['quelle']:
        score = max(score, 8)
        
    return score

def update_file_score(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return 1
        
    # Extract YAML
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        print(f"Skipping {file_path}: No frontmatter found.")
        return 0
        
    frontmatter_block = match.group(1)
    metadata = parse_frontmatter_block(frontmatter_block)

    new_score = calculate_initial_score(metadata)
    
    # Update or add lore_trust
    if 'lore_trust' in metadata:
        try:
            current_score = int(metadata['lore_trust'])
            # Don't overwrite higher user-assigned scores automatically
            if current_score >= new_score:
                print(f"Score for {file_path} is already {current_score} (>= calculated {new_score}). Skipping.")
                return 0
        except ValueError:
            pass
            
    # Simple replace logic
    if 'lore_trust:' in frontmatter_block:
        new_yaml = re.sub(r'lore_trust:\s*\d+', f'lore_trust: {new_score}', frontmatter_block)
    else:
        new_yaml = frontmatter_block.rstrip() + f'\nlore_trust: {new_score}'
        
    new_content = f"--- \n{new_yaml}\n---" + content[match.end():]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Updated score for {file_path} to {new_score}.")
    return 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        if os.path.exists(target_file):
            sys.exit(update_file_score(target_file))
        else:
            print(f"File not found: {target_file}")
            sys.exit(1)
    else:
        print("Usage: python3 lore_score_manager.py <file>")
        sys.exit(1)
