<div align="center">
  <img src="assets/icon.ico" alt="Logo" width="100"/>
  <h1>✈️ WT 3D Scale Model Manager 🚜🚢</h1>
  <p><strong>By Pelad0o</strong></p>
  <p><em>The ultimate tool for extracting, scaling, and segmenting War Thunder vehicles for 3D Printing and Scale Modeling.</em></p>

  [![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
  [![VirusTotal](https://img.shields.io/badge/Security-VirusTotal_Verified-brightgreen.svg)](#-security-trust--zero-false-positives-virustotal)

  [![Invitame un café en cafecito.app](https://cdn.cafecito.app/imgs/buttons/button_6.svg)](https://cafecito.app/gsebastianlopezillia)
</div>

---

*Note: Para leer este manual en español, desliza hacia la mitad de la página.*

---

# 🇬🇧 English User Manual

## 🌟 Introduction

Welcome to the **WT 3D Scale Model Manager**! If you are a **3D printing** (FDM or Resin) enthusiast and love **scale modeling**, this tool allows you to extract, scale to exact dimensions, and segment into printable parts any vehicle (aircraft, tank, or ship) directly from your **War Thunder** installation.

It runs locally as a lightweight background server and provides a state-of-the-art interactive web interface to search, preview, customize, and download files.

---

## ✨ Key Features

- 🔍 **Automatic Detection**: Finds your War Thunder installation and indexes all vehicles instantly.
- 📐 **True-to-Scale Accuracy**: Output models in precise modeler scales (1:35, 1:48, 1:72, 1:100) or set exact mm target dimensions (e.g. 300mm wingspan/length).
- 🧩 **Smart Segmentation**: Choose between monolithic blocks for fast FDM prints, or exploded assemblies (functional parts like turrets, flaps, propellers, wheels separated) for resin and detailed builds.
- 💥 **Damage Variants**: Choose to export pristine models or battle-damaged variants.
- 🖥️ **Interactive 3D Workspace**: Preview parts, explode views, and isolate components right from your browser.
- 🔌 **Portable & Clean**: Runs from a single ZIP file without installing Python or dependencies on your system.

---

## 🛡️ Security, Trust & Zero False Positives (VirusTotal)

**No Executable, No Installer, No False Positives.**

In previous versions, we packaged this application as a standalone `.exe` using `PyInstaller`. However, antivirus engines (including Windows Defender/SmartScreen) frequently flag such executables as "false positives". This happens because malware creators also use PyInstaller to package scripts, causing generic heuristic flags.

**Our Safe & Clean Solution:**
To guarantee absolute security, this version is distributed as a **Portable ZIP** powered by the **official, unmodified, and signed Python embeddable binaries** directly from the Python Software Foundation (python.org).
- **Zero False Positives:** Since we run the web server scripts directly using the official, trusted Python interpreter, it will not trigger antivirus warnings.
- **VirusTotal Verified:** You can upload the entire ZIP or any individual file (including `Iniciar_App.bat`) to [VirusTotal](https://www.virustotal.com/) to verify it. It has a **0/70+ clean score (100% Clean)**.
- **100% Transparent:** There are no compiled binaries of our own. You can audit every line of `web_server.py` and the `Iniciar_App.bat` launcher script before running them.

---

## 🚀 How to Use (No Installation Required)

You do **not** need to install Python, Git, or run command-line terminal commands.

### Step 1: Download & Extract
1. Download the latest `WT_3D_Manager_Portable.zip` release.
2. Extract the ZIP file's contents into any folder on your computer.

### Step 2: Run the App
- Double-click the file named **`Iniciar_App.bat`**.
- This will open a command prompt window starting the local server.

### Step 3: Select War Thunder Folder
- The app will automatically try to find where War Thunder is installed (checking Windows Registry, Steam libraries, and common folders).
- **If it cannot find it automatically**, a standard folder selection window will pop up. Simply select your main `War Thunder` game folder (the one containing the `launcher.exe` file and `content` folder).

### Step 4: Access the Web Interface
- Once initialized, your web browser will automatically open:
   👉 **[http://localhost:8000](http://localhost:8000)**
- You can now browse all vehicles, adjust scales, view exploded parts, and generate them!

### Step 5: Auto-Shutdown (Watchdog)
- When you are done, simply **close the browser tab**.
- The server will detect that the tab was closed and will automatically shut down the command prompt window within a few seconds!

VIDEO: https://youtu.be/YMLJ9H8MjpA
---

## 📐 3D Printing & Scale Modeling Guide

### ⚠️ Important Notice: Game Meshes vs. Printable 3D Models

> [!WARNING]
> **PLEASE READ BEFORE PRINTING TO AVOID FRUSTRATION:**
> The 3D models extracted from the game are originally designed for **real-time 3D rendering**, not for physical 3D printing.
> - **What this means:** Game models contain "shell" geometries (zero-thickness surfaces like wings, plates, or flags), non-manifold edges, open boundaries, and intersecting meshes. Slicing software (such as Cura, PrusaSlicer, OrcaSlicer, or Bambu Studio) requires "watertight" (solid manifold) volume geometries to slice correctly.
> - **Recommended Workflow:** Before sending the files to your slicer, we highly recommend opening the generated `.obj` files in 3D modeling/repair software (like **Windows 3D Builder** (fastest & easiest), **Blender**, **Autodesk Meshmixer**, or **Fusion 360**) to close open meshes, solidify thin sheets (add thickness to wings, armor panels, and propellers), merge intersections, and run automatic mesh repair routines (e.g., "Make Solid" or "Shrinkwrap" tools) to make them manifold and fully ready for successful printing.

### 1. Search and Select your Vehicle
In the left sidebar, use the search box (e.g., *Bf 109*, *Sherman*, *Fletcher*) or use the tabs (**Aircraft**, **Tanks**, **Ships**) to filter the list. Click on a vehicle to load its interactive 3D view.

### 2. Exact Physical Scale Adjustment
Instead of guessing sizes in your slicer, the manager calculates real-world printing dimensions:
- **Standard Proportional Scale (Recommended):** Choose traditional scale modeling sizes from the dropdown list (e.g. `1:35` for tanks, `1:48` / `1:72` for aircraft).
- **Target Dimension Scale:** Set a specific wingspan/length in millimeters and the tool will scale all parts proportionally.

### 3. Segmentation Level
Game 3D models come fused as a single complex block. This option splits the model automatically for easy printing and painting:
- **Level 1 (Decorative / Fused):** Fuses the entire vehicle into a solid block. Perfect for fast FDM prints.
- **Level 2 (Static / Semi-Exploded):** Logically separates large components from small ones (wings together, wheels/propellers separated).
- **Level 3 (Functional / Full Exploded):** Fully disassembles the vehicle into individual pieces (flaps, ailerons, rudders, hatches). Preferred for advanced modelers.

### 4. Explode View & Generate
Use the **Explode View** slider to see how the pieces fit together. You can uncheck parts you don't want to print in the list (like weapons/bombs). Once ready, click **Generate Parts** to slice the model and download the `.obj` files.

---

## ☕ Support the Project

Developing and maintaining this tool takes countless hours of reverse-engineering game files, writing custom parsers, and testing 3D slicing layouts. If this manager saved you time, made your modeling workflow easier, or helped you print your favorite vehicle, please consider supporting my work!

* **For international users**: If you find this tool helpful, a star on GitHub or a shout-out is highly appreciated!
* **For Argentine users (Cafecito)**: You can buy me a coffee to support the developer directly:
  
  [![Invitame un café en cafecito.app](https://cdn.cafecito.app/imgs/buttons/button_6.svg)](https://cafecito.app/gsebastianlopezillia)

---

## ⚖️ Legal Disclaimer (Gaijin EULA & Trademarks)

This software is an unofficial, community-driven open-source project. Please read the following legal notice carefully:

1. **No Affiliation**: This project is **not** affiliated, authorized, associated, sponsored, endorsed by, or in any way officially connected with Gaijin Entertainment, Gaijin Network Ltd., or any of their subsidiaries or affiliates.
2. **Intellectual Property & Trademarks**: "War Thunder", the War Thunder logo, and all related vehicle designs, names, and assets are trademarks or registered trademarks of Gaijin Entertainment. Their use in this application is strictly for identification, description, and educational purposes.
3. **No Asset Distribution**: This repository **does not** contain, package, copy, or distribute any proprietary assets. The tool runs purely as a local script that parses resources already present on the user's personal machine.
4. **User Responsibility**: Extracting, copying, or modifying game assets from the War Thunder client may violate Gaijin's End User License Agreement (EULA). The user assumes all legal and technical risks associated with its execution.
5. **Strictly Non-Commercial**: This tool is designed solely for personal, educational, and recreational scale modeling and 3D printing.
6. **No Warranty**: This tool is provided "as is", without warranty of any kind, express or implied.

---
---

# 🇪🇸 Manual de Usuario en Español

## 🌟 Introducción

¡Bienvenido al **WT 3D Scale Model Manager**! Si eres entusiasta de las **impresoras 3D** (FDM o Resina) y del **modelismo a escala**, esta herramienta te permitirá extraer, escalar a dimensiones exactas y segmentar en piezas imprimibles cualquier vehículo (avión, tanque o barco) directamente desde tu instalación de **War Thunder**.

El programa se ejecuta localmente como un servidor ligero en segundo plano y te proporciona una interfaz web interactiva de última generación para buscar, previsualizar, personalizar y descargar los modelos.

---

## ✨ Características Principales

- 🔍 **Detección Automática**: Encuentra tu instalación de War Thunder e indexa todos los vehículos al instante.
- 📐 **Escala Física Exacta**: Genera modelos en escalas tradicionales (1:35, 1:48, 1:72, 1:100) o define medidas exactas en milímetros (ej. 300mm de envergadura o largo).
- 🧩 **Segmentación Inteligente**: Elige entre bloques fusionados para impresiones FDM rápidas, o despieces completos (partes funcionales separadas como ruedas, flaps, hélices o torretas) ideales para resina y modelos detallados.
- 💥 **Variantes de Daño**: Elige exportar modelos en estado intacto o variantes con daños de batalla.
- 🖥️ **Espacio de Trabajo 3D Interactivo**: Previsualiza las piezas, usa la vista explotada y oculta componentes directamente desde tu navegador.
- 🔌 **Portable y Limpio**: Se ejecuta desde un único archivo ZIP sin necesidad de instalar Python ni librerías en tu sistema.

---

## 🛡️ Seguridad, Confianza y Cero Falsos Positivos (VirusTotal)

**Sin Ejecutables Extraños, Sin Instaladores, Cero Falsos Positivos.**

En versiones anteriores, empaquetábamos esta aplicación como un `.exe` independiente usando `PyInstaller`. Sin embargo, los motores antivirus (incluido Windows Defender/SmartScreen) suelen marcar estos ejecutables como "falsos positivos". Esto ocurre porque los creadores de malware también usan PyInstaller para ocultar sus scripts, lo que genera alertas genéricas basadas en heurística de archivo empaquetado.

**La Solución Segura y Limpia:**
Para garantizar la máxima seguridad y transparencia, esta versión se distribuye como un **ZIP Portable** que contiene y utiliza los **binarios oficiales, inalterados y firmados digitalmente de Python** descargados directamente de la Python Software Foundation (python.org).
- **Cero Falsos Positivos:** Dado que ejecutamos los scripts del servidor web directamente a través del intérprete oficial y de confianza de Python, no se activará ninguna alerta antivirus.
- **Verificación en VirusTotal:** Te invitamos a subir el archivo ZIP completo o cualquier archivo individual (incluyendo `Iniciar_App.bat`) a [VirusTotal](https://www.virustotal.com/) para verificar su integridad. Obtendrás un resultado de **0/70+ alertas (100% limpio)**.
- **100% Transparente:** No hay binarios compilados propios. Puedes auditar cada línea de `web_server.py` y el script `Iniciar_App.bat` antes de ejecutarlos.

---

## 🚀 Instrucciones de Uso (Sin Instalación)

**No** necesitas instalar Python, ni Git, ni ejecutar comandos en la terminal.

### Paso 1: Descargar y Descomprimir
1. Descarga la última versión de `WT_3D_Manager_Portable.zip`.
2. Descomprime su contenido en cualquier carpeta de tu computadora.

### Paso 2: Iniciar la Aplicación
- Haz doble clic en el archivo llamado **`Iniciar_App.bat`**.
- Esto abrirá una ventana de comandos de Windows (consola) que iniciará el servidor local.

### Paso 3: Seleccionar la Carpeta de War Thunder
- El programa intentará encontrar automáticamente dónde está instalado tu War Thunder (buscando en el Registro de Windows, bibliotecas de Steam y rutas comunes).
- **Si no lo encuentra de forma automática**, se abrirá una ventana emergente. Simplemente selecciona la carpeta principal de tu juego `War Thunder` (la que contiene el archivo `launcher.exe` y la carpeta `content`).

### Paso 4: Usar la Interfaz Web
- Una vez inicializado, tu navegador web se abrirá automáticamente en:
   👉 **[http://localhost:8000](http://localhost:8000)**
- ¡Ya puedes explorar los vehículos, ajustar la escala, ver el despiece y generar las piezas!

### Paso 5: Apagado Automático (Watchdog)
- Cuando termines, simplemente **cierra la pestaña de tu navegador**.
- El servidor detectará que la pestaña fue cerrada y cerrará la ventana de comandos de la consola automáticamente en pocos segundos.

---

## 📐 Guía de Impresión 3D y Modelismo

### ⚠️ Nota Importante: Modelos de Juego vs. Modelos Imprimibles

> [!WARNING]
> **POR FAVOR, LEE ESTO ANTES DE IMPRIMIR PARA EVITAR FRUSTRACIONES:**
> Los modelos 3D extraídos del juego están diseñados originalmente para **renderizado en tiempo real** (gráficos de computadora), no para impresión 3D física.
> - **Qué significa esto:** Los modelos del juego contienen geometrías tipo "cáscara" (superficies con grosor cero como alas, chapas o banderas), bordes no maniformes, mallas abiertas e intersecciones internas. Los laminadores (como Cura, PrusaSlicer, OrcaSlicer o Bambu Studio) necesitan volúmenes cerrados y herméticos ("watertight" o sólidos maniformes) para rebanar correctamente.
> - **Flujo de trabajo recomendado:** Antes de mandar las piezas al laminador, te recomendamos abrir los archivos `.obj` generados en un software de reparación o modelado 3D (como **Windows 3D Builder** (el más rápido y fácil de usar), **Blender**, **Autodesk Meshmixer** o **Fusion 360**) para cerrar las mallas abiertas, darles grosor físico a las superficies delgadas (como hélices, alerones o chapas), fusionar intersecciones y realizar una reparación de malla sólida (usando herramientas como "Make Solid" o "Sólido rápido") para dejarlas listas para una impresión exitosa.

### 1. Buscar y Seleccionar tu Vehículo
En la barra lateral izquierda, usa el buscador (ej. *Bf 109*, *Sherman*, *Fletcher*) o usa las pestañas (**Aviones**, **Tanques**, **Barcos**) para filtrar la lista. Haz clic sobre un vehículo para cargar su vista 3D interactiva.

### 2. Ajuste de Escala Física Exacta
En lugar de adivinar el tamaño en tu laminador (Slicer), el gestor calcula las dimensiones reales de impresión:
- **Escala Proporcional Estándar (Recomendado):** Selecciona escalas de modelismo tradicionales (ej. `1:35` para vehículos terrestres, `1:48` / `1:72` para aviones).
- **Escala por Medida Objetivo:** Define una medida específica de envergadura o largo en milímetros y la herramienta escalará todas las partes proporcionalmente.

### 3. Nivel de Segmentación
Los modelos de juego vienen en un solo bloque complejo. Esta opción los divide de forma automática para facilitar la impresión y pintura:
- **Nivel 1 (Decorativo / Fusionado):** Fusiona todo el vehículo en un bloque sólido y robusto. Ideal para impresiones FDM rápidas de una sola pieza.
- **Level 2 (Estático / Semi-despiezado):** Separa las partes grandes de las pequeñas de forma lógica (ej. alas y fuselaje unidos, pero hélice y ruedas separadas).
- **Level 3 (Funcional / Despiece total):** Desarma por completo el vehículo en piezas individuales (flaps, alerones, timones, escotillas). Preferido por modelistas avanzados.

### 4. Vista Explotada y Generar
Usa el deslizador de **Vista Explotada** para ver cómo encajan las piezas. Puedes desmarcar las casillas en la lista para ocultar partes que no quieras imprimir (como bombas o cohetes). Al finalizar, haz clic en **Generar Piezas** para procesar el modelo y descargar los archivos `.obj`.

VIDEO: https://youtu.be/YMLJ9H8MjpA
---

## ☕ Apoya el Proyecto (Cafecito)

El desarrollo y mantenimiento de esta herramienta requiere de incontables horas invertidas en hacer ingeniería inversa de formatos propietarios del juego, programar los conversores 3D y diseñar y probar el despiece de los modelos.

Si este gestor te ahorró horas de modelado en Blender, te facilitó el laminado de piezas o te ayudó a imprimir tu vehículo preferido de War Thunder, **¡invitame un Cafecito!** Tu aporte ayuda un montón a poder seguir mejorando la herramienta y sumar soporte para nuevos vehículos:

[![Invitame un café en cafecito.app](https://cdn.cafecito.app/imgs/buttons/button_6.svg)](https://cafecito.app/gsebastianlopezillia)

---

## ⚖️ Descargo de Responsabilidad Legal (EULA de Gaijin y Marcas)

Este software es un proyecto de código abierto no oficial desarrollado por la comunidad. Por favor, lee atentamente el siguiente aviso legal:

1. **Sin Afiliación**: Este proyecto **no** está afiliado, ni autorizado, asociado, patrocinado, respaldado ni conectado de ninguna manera oficial con Gaijin Entertainment, Gaijin Network Ltd., ni ninguna de sus subsidiarias o filiales.
2. **Propiedad Intelectual y Marcas**: "War Thunder", el logotipo de War Thunder y todos los diseños, nombres y recursos de vehículos relacionados son marcas comerciales o registradas de Gaijin Entertainment. Su uso en esta aplicación es estrictamente para fines de identificación, descripción y educación.
3. **Sin Distribución de Recursos**: Este repositorio **no** contiene, empaqueta, copia ni distribuye ningún recurso propietario. La herramienta funciona exclusivamente como un script local que analiza recursos que ya se encuentran presentes en la máquina personal del usuario.
4. **Responsabilidad del Usuario**: La extracción, copia o modificación de recursos del juego desde el cliente de War Thunder puede violar el Acuerdo de Licencia de Usuario Final (EULA). El usuario asume todos los riesgos legales y técnicos asociados con su ejecución.
5. **Uso Estrictamente No Comercial**: Esta herramienta está deñada únicamente para fines de modelismo a escala e impresión 3D de carácter personal, educativo y recreativo.
6. **Sin Garantías**: Esta herramienta se proporciona "tal cual" (as is), sin garantía de ningún tipo, expresa o implícita.

---

## 📩 Contacto / Contrataciones

Creado y mantenido por **Pelad0o**.
* **Gamer Tag:** `Pelad0o`
* **Correo electrónico de contacto:** [gsebastianlopezillia@gmail.com](mailto:gsebastianlopezillia@gmail.com)
