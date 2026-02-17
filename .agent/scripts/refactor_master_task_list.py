import re

def refactor_master_task_list(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find the historical phases section
    # Usually starts after Phase 1.12 or similar
    # We want to group all "Phase X" sections from the bottom
    
    sections = re.split(r'\n(?=### Phase )', content)
    
    header = sections[0]
    phases = sections[1:]
    
    new_phases = []
    for i, phase in enumerate(phases):
        # We want to keep Phase 1.13 or very recent ones open?
        # Let's say we keep the top 2 phases open, rest in details
        # Wait, the list is growing from the bottom? No, Phase 1.12 is near top of historical section.
        
        # In MASTER_TASK_LIST.md, the phases are listed newest first.
        # Phase 1.12, 1.11, etc.
        
        lines = phase.strip().split('\n')
        phase_header = lines[0].strip()
        phase_body = '\n'.join(lines[1:]).strip()
        
        is_open = " open" if i < 2 else ""
        new_phases.append(f'<details{is_open}>\n<summary><b>{phase_header.replace("### ", "")}</b></summary>\n\n{phase_body}\n</details>')

    final_content = header.strip() + "\n\n---\n\n" + "\n\n".join(new_phases) + "\n"
    
    with open(filepath + ".refactored", 'w') as f:
        f.write(final_content)

if __name__ == "__main__":
    refactor_master_task_list("MASTER_TASK_LIST.md")
