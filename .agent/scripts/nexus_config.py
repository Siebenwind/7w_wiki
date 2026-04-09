import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "lore_manifest.json"

def load_nexus():
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r") as f:
            return json.load(f)
    return {}

config = load_nexus()
lore = config.get("lore", {})

WORLD_NAME = lore.get("world_name", "Siebenwind")
CHRONOLOGY = lore.get("chronology", "Sonnenzirkel")
TONE = lore.get("tone", "immersiv, historisch")

directories = lore.get("directories", {})
WIKI_DIR_NAME = directories.get("wiki", "docs/Siebenwind_Wiki")
SOURCES_DIR_NAME = directories.get("sources", "Quellen")

WIKI_DIR = REPO_ROOT / WIKI_DIR_NAME
SOURCES_DIR = REPO_ROOT / SOURCES_DIR_NAME
