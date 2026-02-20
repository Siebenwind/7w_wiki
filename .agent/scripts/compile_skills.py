#!/usr/bin/env python3
import os
import json
import glob
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "lore_manifest.json"

def load_config():
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r") as f:
            return json.load(f)
    return {}

def compile_skills():
    config = load_config()
    lore_config = config.get("lore", {})
    
    # Default variables
    variables = {
        "{{WORLD_NAME}}": lore_config.get("world_name", "Siebenwind"),
        "{{CHRONOLOGY}}": lore_config.get("chronology", "Sonnenzirkel"),
        "{{TONE}}": lore_config.get("tone", "immersiv, historisch"),
    }
    
    skills_dir = REPO_ROOT / ".agent" / "skills"
    tpl_files = glob.glob(str(skills_dir / "**" / "SKILL.md.tpl"), recursive=True)
    
    compiled_count = 0
    for tpl_path in tpl_files:
        tpl_file = Path(tpl_path)
        dest_file = tpl_file.with_suffix("") # Remove .tpl
        
        with open(tpl_file, "r") as f:
            content = f.read()
            
        for key, value in variables.items():
            content = content.replace(key, value)
            
        with open(dest_file, "w") as f:
            f.write(content)
            
        print(f"Compiled: {dest_file.relative_to(REPO_ROOT)}")
        compiled_count += 1
        
    print(f"Successfully compiled {compiled_count} SKILL files.")

if __name__ == "__main__":
    compile_skills()
