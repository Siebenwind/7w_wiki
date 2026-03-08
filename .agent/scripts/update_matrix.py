#!/usr/bin/env python3
"""
Updates the SY_WORKFLOW_CLI_MATRIX.md file by checking for any unlisted workflows 
in .agent/workflows/ and appending them to the table.
"""
import os
import re

WORKFLOWS_DIR = ".agent/workflows"
MATRIX_FILE = "System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md"

def update_matrix():
    if not os.path.exists(MATRIX_FILE):
        print(f"Error: {MATRIX_FILE} not found.")
        return

    with open(MATRIX_FILE, "r") as f:
        content = f.read()

    # Find all currently documented workflows
    documented = set(re.findall(r"\| `/(.*?)` \|", content))
    
    # Find all actual workflows
    actual = set()
    for fname in os.listdir(WORKFLOWS_DIR):
        if fname.endswith(".md"):
            actual.add(fname[:-3])

    missing = actual - documented
    if not missing:
        print("Matrix is up-to-date. No missing workflows found.")
        return

    print(f"Found {len(missing)} unlisted workflows. Appending to matrix...")
    
    with open(MATRIX_FILE, "a") as f:
        for wf in sorted(missing):
            f.write(f"| `/{wf}` | TBD | TBD | Auto-detected (please update) |\n")
            
    print("Done. Please review the updated matrix.")

if __name__ == "__main__":
    update_matrix()
