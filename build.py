import os
import subprocess
import sys

def main():
    print("Installing PyInstaller if needed...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "pillow"])
    
    print("\nBuilding WT_3D_Manager.exe...")
    
    # Check if thumbnails dir exists
    thumbnails_src = os.path.join("Bf109_Raw_Asset", "thumbnails")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--console",  # We keep console so they can see progress/errors
        "--icon=icon.ico",
        "--name=WT_3D_Manager",
        "--paths=lib",
        "--paths=lib\\dae",
        "--add-data=lib;lib",
        "--add-data=index.html;.",
        "--add-data=style.css;.",
    ]
    
    if os.path.exists(thumbnails_src):
        cmd.append(f"--add-data={thumbnails_src};thumbnails")
    else:
        print(f"Warning: {thumbnails_src} not found. Thumbnails won't be bundled.")
        
    cmd.append("web_server.py")
    
    subprocess.check_call(cmd)
    
    print("\nBuild complete! Check the 'dist' folder for WT_3D_Manager.exe")

if __name__ == "__main__":
    main()
