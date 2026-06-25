<div align="center">
  <img src="assets/icon.ico" alt="Logo" width="100"/>
  <h1>✈️ WT 3D Scale Model Manager 🚜🚢</h1>
  <p><strong>By Pelad0o</strong></p>
  <p><em>The ultimate tool for extracting, scaling, and segmenting War Thunder vehicles for 3D Printing and Scale Modeling.</em></p>

  [![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
  [![VirusTotal](https://img.shields.io/badge/Security-VirusTotal_Verified-brightgreen.svg)](#-security--trust-virustotal--signpath)
</div>

---

## 🌟 Introduction

Welcome to the **WT 3D Scale Model Manager**! If you are a **3D printing** (FDM or Resin) enthusiast and love **scale modeling**, this tool allows you to extract, scale to exact dimensions, and segment into printable parts any vehicle (aircraft, tank, or ship) directly from your **War Thunder** installation.

![App Demo](assets/demo.gif)
*(Placeholder for Demo GIF showing the interface and 3D preview. You can record a short screen capture and save it as `assets/demo.gif`)*

---

## ✨ Key Features

- 🔍 **Automatic Detection**: Finds your War Thunder installation and indexes all vehicles instantly.
- 📐 **True-to-Scale Accuracy**: Output models in precise modeler scales (1:35, 1:48, 1:72) or set exact mm target dimensions (e.g. 300mm wingspan).
- 🧩 **Smart Segmentation**: Choose between monolithic blocks for FDM, or exploded assemblies (functional parts like turrets, flaps, propellers separated) for resin and complex builds.
- 💥 **Damage Variants**: Choose to export pristine models or battle-damaged variants.
- 🖥️ **Interactive 3D Workspace**: Preview parts, explode views, and isolate components right from your browser.

![Feature Screenshot](assets/screenshot_explode.png)
*(Placeholder for Explode View Screenshot. Take a screenshot of the 3D viewer and save it as `assets/screenshot_explode.png`)*

---

## 🛡️ Security & Trust (VirusTotal & SignPath)

We take security seriously. Because this application is packaged as a standalone executable using `PyInstaller`, some overzealous antivirus software (including Windows SmartScreen) might flag it as a "false positive".

**Why does this happen?**
PyInstaller bundles a Python environment into a `.exe`. Because malware authors sometimes use the same tool to hide malicious scripts, antivirus heuristics often flag *any* unknown PyInstaller executable by default.

**Our Guarantee:**
1. **[VirusTotal Scan](https://www.virustotal.com/)**: Every release is scanned through VirusTotal. We invite you to upload `WT_3D_Manager.exe` to VirusTotal to verify its integrity. *(Note for dev: Link the specific report URL here once released)*
2. **SignPath Certification**: We are currently in the process of applying for a **SignPath Code Signing Certificate** for open-source projects. Once approved, the executable will be digitally signed to completely eliminate Windows SmartScreen warnings and prove our identity as the authors.
3. **Open Source**: The code is fully open-source. You can read every line of `web_server.py` and run it yourself if you prefer not to use the `.exe`.

---

## 🛠️ Installation Guide for Non-Programmers

Don't worry, you don't need any coding skills or Python installed to run this tool. Just follow these simple steps:

### Step 1: Download the App
1. Download the latest `WT_3D_Manager.zip` release and extract it.

### Step 2: Run the Manager!
* On Windows, simply double-click `WT_3D_Manager.exe`.
* **What it does automatically:**
  * Creates your local `config.json` file.
  * Automatically attempts to find your War Thunder installation. If it cannot find it, it will pop up a window asking you to select the game folder.
  * Launches the local web server and automatically opens the application in your web browser.
  * If the browser does not open automatically, go to:
     👉 **[http://localhost:8000](http://localhost:8000)**

---

## 📐 3D Printing & Scale Modeling Guide

### ⚠️ Important Notice: Game Meshes vs. Printable 3D Models

> [!WARNING]
> **PLEASE READ BEFORE PRINTING TO AVOID FRUSTRATION:**
> The 3D models extracted from the game are originally designed for **real-time 3D rendering**, not for physical 3D printing.
> * **What this means:** Game models contain "shell" geometries (zero-thickness surfaces like wings, plates, or flags), non-manifold edges, open boundaries, and intersecting meshes. Slicing software (such as Cura, PrusaSlicer, OrcaSlicer, or Bambu Studio) requires "watertight" (solid manifold) volume geometries to slice correctly.
> * **The Purpose of this Tool:** These generated `.obj` files serve as an **excellent, highly accurate starting base** so you don't have to model the vehicle from scratch. 
> * **Recommended Workflow:** Before sending the files to your slicer, we highly recommend opening the generated `.obj` files in 3D modeling/repair software (like **Blender**, **Autodesk Meshmixer**, **Windows 3D Builder**, or **Fusion 360**) to close open meshes, solidify thin sheets (add thickness to wings, armor panels, and propellers), merge intersections, and run automatic mesh repair routines (e.g., "Make Solid" or "Shrinkwrap" tools) to make them manifold and fully ready for successful printing.

### 1. Search and Select your Vehicle
In the left sidebar, you will see a list of vehicles detected in your game files. You can use the **Aircraft**, **Tanks**, and **Ships** tabs to narrow the list instantly, or type in the search box (e.g., *Bf 109*, *Sherman*, *Fletcher*). Click on the vehicle to load its interactive 3D view.

### 2. Exact Physical Scale Adjustment
Instead of guessing the size in your slicing software (Slicer), the manager calculates real-world printing dimensions for you:
* **Standard Proportional Scale (Recommended):** Choose traditional scale modeling sizes from the dropdown list.
* **Target Dimension Scale:** If you want your model to have a specific wingspan (e.g., 30 cm / 300 mm) or length, select the corresponding mode and adjust the slider.

### 3. Segmentation Level (Your best ally for printing!)
Game 3D models come fused as a single complex block. This option splits the model automatically for easy printing and painting:
* **Level 1 (Decorative / Fused):** Fuses the entire vehicle into a solid block. Perfect for fast FDM prints.
* **Level 2 (Static / Semi-Exploded):** Logically separates large components from small ones (wings together, wheels/propellers separated).
* **Level 3 (Functional / Full Exploded):** Fully disassembles the vehicle into individual pieces (flaps, ailerons, rudders, hatches). Preferred for advanced modelers.

### 4. Explode View & Generate
Use the **Explode View** slider to see how the pieces fit together. Once ready, click **Generate Parts** to slice the model and download the `.obj` files.

---

## ⚖️ Legal Disclaimer (Gaijin EULA & Trademarks)

This software is an unofficial, community-driven open-source project. Please read the following legal notice carefully:

1. **No Affiliation**: This project is **not** affiliated, authorized, associated, sponsored, endorsed by, or in any way officially connected with Gaijin Entertainment, Gaijin Network Ltd., or any of their subsidiaries or affiliates.
2. **Intellectual Property & Trademarks**: "War Thunder", the War Thunder logo, and all related vehicle designs, names, and assets are trademarks or registered trademarks of Gaijin Entertainment. Their use in this application is strictly for identification, description, and educational purposes.
3. **No Asset Distribution**: This repository **does not** contain, package, copy, or distribute any proprietary assets.
4. **User Responsibility**: Extracting, copying, or modifying game assets from the War Thunder client may violate Gaijin's End User License Agreement (EULA). The user assumes all legal and technical risks associated with its execution.
5. **Strictly Non-Commercial**: This tool is designed solely for personal, educational, and recreational scale modeling and 3D printing.
6. **No Warranty**: This tool is provided "as is", without warranty of any kind, express or implied.

---

## 📩 Contact / Hiring

Created and maintained by **Pelad0o**.
* **Gamer Tag:** `Pelad0o`
* **Contact email:** [gsebastianlopezillia@gmail.com](mailto:gsebastianlopezillia@gmail.com)
