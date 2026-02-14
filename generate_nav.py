import os

def print_nav(docs_dir, base_path="", indent=0):
    full_path = os.path.join(docs_dir, base_path)
    if not os.path.exists(full_path):
        return
        
    items = sorted(os.listdir(full_path))
    
    for item in items:
        if item.startswith(".") or item == "index.md":
            continue
            
        item_path = os.path.join(base_path, item)
        full_item_path = os.path.join(docs_dir, item_path)
        
        if os.path.isdir(full_item_path):
            title = item.split("_", 1)[-1] if "_" in item else item
            print(f"{'  ' * indent}- {title}:")
            # If index exists, add it first
            if os.path.exists(os.path.join(full_item_path, "index.md")):
                print(f"{'  ' * (indent + 1)}- Übersicht: {item_path}/index.md")
            print_nav(docs_dir, item_path, indent + 1)
        elif item.endswith(".md"):
            title = item[:-3].replace("_", " ")
            print(f"{'  ' * indent}- {title}: {item_path}")

docs_dir = "docs"
print_nav(docs_dir, "Siebenwind_Wiki", 2)
