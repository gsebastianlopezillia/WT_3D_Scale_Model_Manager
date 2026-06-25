import os
import subprocess
import sys
import zipfile

def main():
    print("Installing PyInstaller if needed...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "pillow"])
    
    print("\nBuilding WT_3D_Manager.exe...")
    
    # Check if thumbnails dir exists
    thumbnails_src = os.path.join("Bf109_Raw_Asset", "thumbnails")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--console",  # We keep console so they can see progress/errors
        "--icon=assets/icon.ico",
        "--name=WT_3D_Manager",
        "--paths=lib",
        "--paths=lib\\dae",
        "--add-data=lib;lib",
        "--add-data=frontend/index.html;frontend",
        "--add-data=frontend/style.css;frontend",
    ]
    
    if os.path.exists(thumbnails_src):
        cmd.append(f"--add-data={thumbnails_src};thumbnails")
    else:
        print(f"Warning: {thumbnails_src} not found. Thumbnails won't be bundled.")
        
    cmd.append("web_server.py")
    
    subprocess.check_call(cmd)
    
    print("\nCreating ZIP archive...")
    app_dir = os.path.join("dist", "WT_3D_Manager")
    readme_path = "README.md"
    zip_path = os.path.join("dist", "WT_3D_Manager.zip")
    
    if os.path.exists(app_dir):
        import shutil
        if os.path.exists(readme_path):
            shutil.copy(readme_path, app_dir)
            
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(app_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, "dist")
                    zipf.write(file_path, arcname)
                    
        print(f"\nBuild complete! Check the 'dist' folder for {os.path.basename(zip_path)}")
    else:
        print("\nWarning: Build failed. App directory not found. ZIP not created.")

if __name__ == "__main__":
    main()
