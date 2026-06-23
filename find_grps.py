import os
import sys
import json

# Add dagor_explorer/src/dae to python path
try:
    from parse.gameres import GameResourcePack
except ModuleNotFoundError as e:
    print("\n" + "="*80)
    print("ERROR: Required subfolder 'dagor_explorer' not found in path.")
    print(f"Details: {e}")
    print("If you cloned this repository, ensure submodules are updated:")
    print("    git submodule update --init --recursive")
    print("Or if you downloaded the ZIP, run 'run_web_manager.ps1' to clone them automatically.")
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
    content_dir = os.path.join(wt_root, 'content')
    
    if not os.path.exists(content_dir):
        print(f"ERROR: War Thunder content directory not found at {content_dir}")
        return
        
    print(f"Scanning {content_dir} for GRP files...")
    grp_files = []
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.grp'):
                grp_files.append(os.path.join(root, file))
                
    print(f"Found {len(grp_files)} GRP files.")
    
    print("\nListing some GRP files and their resources:")
    for path in grp_files[:15]:
        rel_path = os.path.relpath(path, wt_root)
        try:
            grp = GameResourcePack(path)
            num_res = grp.getRealResEntryCnt()
            print(f"  {rel_path}: {num_res} resources")
            
            # Print a few resource names
            res_names = []
            for i in range(min(5, num_res)):
                res_names.append(grp.getRealResEntry(i).getName())
            print(f"    Sample: {', '.join(res_names)}")
        except Exception as e:
            print(f"  Failed to read {rel_path}: {e}")

if __name__ == "__main__":
    main()
