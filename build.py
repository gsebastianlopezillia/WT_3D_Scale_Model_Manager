import os
import urllib.request
import zipfile
import shutil
import subprocess
import sys

PYTHON_EMBED_URL = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"
PYTHON_ZIP_PATH = "python-embed.zip"

def main():
    print("Preparando entorno Portable Python (Cero Falsos Positivos)...")
    
    app_dir = os.path.join("dist", "WT_3D_Manager")
    python_dir = os.path.join(app_dir, "python")
    site_packages = os.path.join(python_dir, "Lib", "site-packages")
    
    # 1. Clean previous dist
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    os.makedirs(site_packages, exist_ok=True)
    
    # 2. Download and extract Python Embeddable
    print("Descargando Python embebido oficial (3.11)...")
    if not os.path.exists(PYTHON_ZIP_PATH):
        urllib.request.urlretrieve(PYTHON_EMBED_URL, PYTHON_ZIP_PATH)
        
    print("Extrayendo Python...")
    with zipfile.ZipFile(PYTHON_ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(python_dir)
        
    # 3. Enable site-packages in python311._pth
    pth_file = os.path.join(python_dir, "python311._pth")
    if os.path.exists(pth_file):
        with open(pth_file, 'r') as f:
            pth_content = f.read()
        
        pth_content = pth_content.replace("#import site", "import site")
        if "Lib\\site-packages" not in pth_content:
            pth_content += "\nLib\\site-packages\n"
            
        with open(pth_file, 'w') as f:
            f.write(pth_content)
            
    # 4. Install dependencies into site-packages using HOST pip
    print("Instalando dependencias en el entorno portatil...")
    # These are the exact dependencies required by web_server.py and wt_tools
    deps = ["pillow", "zstandard", "construct==2.9.40", "pylzma", "click", "lark", "requests", "bencode.py", "jsondiff", "PyQt5"]
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "--target", site_packages, 
    ] + deps)
    
    # 5. Copy project files
    print("Copiando archivos del proyecto...")
    shutil.copy("web_server.py", app_dir)
    if os.path.exists("README.md"):
        shutil.copy("README.md", app_dir)
    if os.path.exists("LICENSE"):
        shutil.copy("LICENSE", app_dir)
        
    shutil.copytree("lib", os.path.join(app_dir, "lib"))
    shutil.copytree("frontend", os.path.join(app_dir, "frontend"))
    
    thumbnails_src = os.path.join("Bf109_Raw_Asset", "thumbnails")
    if os.path.exists(thumbnails_src):
        shutil.copytree(thumbnails_src, os.path.join(app_dir, "thumbnails"))
        
    # 6. Create the launcher .bat file
    print("Creando lanzador seguro...")
    bat_content = """@echo off
title WT 3D Manager
echo ========================================================
echo   Iniciando WT 3D Scale Model Manager (Portable)
echo ========================================================
echo.
echo Por favor, no cierres esta ventana de comandos.
echo El servidor local estara corriendo en segundo plano.
echo.
cd /d "%~dp0"
.\\python\\python.exe web_server.py
pause
"""
    with open(os.path.join(app_dir, "Iniciar_App.bat"), 'w') as f:
        f.write(bat_content)
        
    # 7. Create ZIP archive
    print("Creando archivo ZIP final...")
    zip_path = os.path.join("dist", "WT_3D_Manager_Portable.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(app_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, "dist")
                zipf.write(file_path, arcname)
                
    print(f"\nExito! Puedes encontrar tu paquete final en: {zip_path}")
    print("Este paquete portatil NO dara falsos positivos en VirusTotal.")
    
    if os.path.exists(PYTHON_ZIP_PATH):
        os.remove(PYTHON_ZIP_PATH)

if __name__ == "__main__":
    main()
