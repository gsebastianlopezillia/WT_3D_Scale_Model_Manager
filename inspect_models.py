import os
import sys

# Add dagor_explorer/src/dae to python path
sys.path.append(os.path.abspath(r'.\dagor_explorer\src\dae'))

from parse.gameres import GameResDesc

def main():
    wt_root = r'D:\Juegos\steam\steamapps\common\War Thunder'
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
