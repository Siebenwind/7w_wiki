import os
import re
import yaml

def calculate_initial_score(metadata):
    """Calculates entry score based on epistemic rank."""
    ranks = {
        '#user_canon': 10,
        '#canon': 8,
        '#bote': 5,
        '#überlieferung': 3,
        '#perspektive': 2
    }
    
    status = metadata.get('status', '#perspektive')
    score = ranks.get(status, 1)
    
    # Bonuses
    if metadata.get('quelle') and 'Hintergrund' in metadata['quelle']:
        score = max(score, 8)
        
    return score

def update_file_score(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract YAML
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return
        
    try:
        metadata = yaml.safe_load(match.group(1))
    except:
        return

    new_score = calculate_initial_score(metadata)
    
    # Update or add lore_trust
    if 'lore_trust' in metadata:
        # Don't overwrite higher user-assigned scores automatically
        if metadata['lore_trust'] >= new_score:
            return
            
    # Simple replace logic for simulation (ideally use a YAML parser that preserves comments)
    if 'lore_trust:' in match.group(1):
        new_yaml = re.sub(r'lore_trust: \d+', f'lore_trust: {new_score}', match.group(1))
    else:
        new_yaml = match.group(1) + f'\nlore_trust: {new_score}'
        
    new_content = f"--- \n{new_yaml.strip()}\n---" + content[match.end():]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    # Placeholder for batch processing
    print("Lore Score Manager initialized.")
