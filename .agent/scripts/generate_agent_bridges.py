#!/usr/bin/env python3
"""
Generates external bridge files in .agents/skills/ for any core skill in .agent/skills/ 
that doesn't already have one. This allows external agents to discover the wiki's internal capabilities.
"""
import os
import re

CORE_SKILLS_DIR = ".agent/skills"
BRIDGE_SKILLS_DIR = ".agents/skills"

def extract_title(filepath):
    if not os.path.exists(filepath):
        return "Unknown Skill"
    
    with open(filepath, "r") as f:
        content = f.read()
    
    # Try to find a yaml name
    name_match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    if name_match:
        return name_match.group(1).strip()
    
    # Try to find an H1
    h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    
    return "Unknown Skill"

def generate_bridges():
    os.makedirs(BRIDGE_SKILLS_DIR, exist_ok=True)
    generated_count = 0
    
    for item in os.listdir(CORE_SKILLS_DIR):
        core_skill_path = os.path.join(CORE_SKILLS_DIR, item)
        if not os.path.isdir(core_skill_path):
            continue
            
        core_skill_file = os.path.join(core_skill_path, "SKILL.md")
        if not os.path.exists(core_skill_file):
            continue
            
        bridge_skill_path = os.path.join(BRIDGE_SKILLS_DIR, item)
        bridge_skill_file = os.path.join(bridge_skill_path, "SKILL.md")
        
        # Don't overwrite existing bridges (like art_director or stats)
        if os.path.exists(bridge_skill_file):
            continue
            
        # Extract name
        skill_name = extract_title(core_skill_file)
        
        # Create directory
        os.makedirs(bridge_skill_path, exist_ok=True)
        
        # Write bridge file
        bridge_content = f"""---
name: {skill_name} Bridge
description: Auto-generated external visibility bridge for {skill_name}.
---

# Skill: {skill_name} (External Bridge)
> **Wrapper for**: `.agent/skills/{item}/SKILL.md`

This is an auto-generated bridge file. Its sole purpose is to make the internal skill capabilities discoverable to external agents (like Jules, Claude, or Gemini).

## ⚠️ Mandatory Usage Instruction
To understand the actual capabilities, constraints, and runtime commands for this skill, **you MUST explicitly read the internal target file**: 
`{core_skill_file}`

Do not attempt to guess the functionality based on this bridge file.
"""
        with open(bridge_skill_file, "w") as f:
            f.write(bridge_content)
            
        print(f"Generated bridge for: {item}")
        generated_count += 1
        
    print(f"Successfully generated {generated_count} new bridge skills.")

if __name__ == "__main__":
    generate_bridges()
