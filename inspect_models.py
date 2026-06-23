import os
import sys
import json

# Add local vendored libraries to python path
sys.path.append(os.path.abspath(r'.\lib\dae'))

try:
    from parse.gameres import GameResDesc
except ModuleNotFoundError as e:
    print("\n" + "="*80)
    print("ERROR: Missing required vendored dependencies in the 'lib/' folder.")
    print(f"Details: {e}")
    print("Please make sure the repository was cloned completely with the 'lib/' directory.")
    print("="*80 + "\n")
    sys.exit(1)

def main():
    # Load path settings from config.json if it exists, otherwise use defaults
    config = {
        "wt_root": r'C:\Program Files (x86)\Steam\steamapps\common\War Thunder'
    }
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                if "wt_root" in user_config: config["wt_root"] = user_config["wt_root"]
                elif "WT_ROOT" in user_config: config["wt_root"] = user_config["WT_ROOT"]
        except Exception as e:
            print(f"Error loading config.json: {e}")

    wt_root = config["wt_root"]
    desc_path = os.path.join(wt_root, r'content\base\res\dynModelDesc.bin')
    
    if not os.path.exists(desc_path):
        print(f"ERROR: Descriptor file not found at {desc_path}")
        return
        
    print("Loading dynModelDesc.bin...")
    desc = GameResDesc(desc_path)
    desc.loadDataBlock()
    blk = desc.getDataBlock()
    
    # Print root structure of data block
    children = blk.getChildren()
    print(f"DataBlock loaded. Root children count: {len(children)}")
    
    # List some names
    names = []
    for child in children[:50]:
        names.append(child.getName())
        
    print("First 50 vehicle/model names:")
    print(", ".join(names))

if __name__ == "__main__":
    main()
