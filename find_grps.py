import os
import sys

# Add dagor_explorer/src/dae to python path
sys.path.append(os.path.abspath(r'.\dagor_explorer\src\dae'))

from parse.gameres import GameResourcePack

def main():
    wt_root = r'D:\Juegos\steam\steamapps\common\War Thunder'
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
