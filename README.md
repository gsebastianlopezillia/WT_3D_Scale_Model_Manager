# ✈️ WT 3D Scale Model Manager (by Pelad0o) 🚜🚢

Welcome to the **WT 3D Scale Model Manager**! If you are a **3D printing** (FDM or Resin) enthusiast and love **scale modeling**, this tool allows you to extract, scale to exact dimensions, and segment into printable parts any vehicle (aircraft, tank, or ship) directly from your **War Thunder** installation.

*Note: Para leer este manual en español, desliza hacia abajo.*

---

## 🛠️ Installation Guide for Non-Programmers

Don't worry, you don't need any coding skills or Python installed to run this tool. Just follow these simple steps:

### Step 1: Download the App
1. Download the latest `WT_3D_Manager.exe` release (or extract the `.zip`).

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

Once inside the web interface, you'll see a state-of-the-art interactive visual workspace:

### 1. Search and Select your Vehicle
In the left sidebar, you will see a list of vehicles detected in your game files. You can use the **Aircraft**, **Tanks**, and **Ships** tabs to narrow the list instantly, or type in the search box (e.g., *Bf 109*, *Sherman*, *Fletcher*). Click on the vehicle to load its interactive 3D view.

### 2. Exact Physical Scale Adjustment
Instead of guessing the size in your slicing software (Slicer), the manager calculates real-world printing dimensions for you:
* **Standard Proportional Scale (Recommended):** Choose traditional scale modeling sizes from the dropdown list:
  * **1:35** (The gold standard for military ground vehicles/tanks).
  * **1:32 or 1:48** (Excellent scales for detailed aircraft models).
  * **1:72** (Great for quick-to-print aircraft or tank miniatures).
  * **1:100** (Perfect for tabletop wargames).
* **Target Dimension Scale:** If you want your model to have a specific wingspan (e.g., 30 cm / 300 mm) or length, select the corresponding mode and adjust the slider.

### 3. Segmentation Level (Your best ally for printing!)
Game 3D models come fused as a single complex block with internal parts that make them difficult to print. This option splits the model automatically for easy printing and painting:
* **Level 1 (Decorative / Fused):** Fuses the entire vehicle into a solid, robust block. Perfect for fast, single-piece FDM prints or small resin miniatures.
* **Level 2 (Static / Semi-Exploded):** Logically separates large components from small ones. For instance, it keeps the wings and fuselage together but separates the propeller, wheels, and glass canopy. Great for painting parts individually before gluing.
* **Level 3 (Functional / Full Exploded):** Fully disassembles the vehicle into individual pieces (flaps, ailerons, rudders, tank hatches, road wheels, ship turrets, and gun barrels). Preferred for advanced modelers who want to build moving parts, hinges, or fit electronics.

### 4. Battle Damage Variants
Many vehicles have alternative damage meshes in the game files. The tool detects these automatically, allowing you to choose whether to build, for example, a healthy propeller or one bent from a crash landing.

### 5. Explode View
Use the **Explode View** slider at the bottom of the 3D viewport to see how the pieces fit together. This serves as an interactive visual assembly guide after printing. You can also uncheck boxes in the parts checklist to hide parts you don't want to print (like combat payloads or bombs).

### 6. Generate and Download
1. Once your scale and segmentation settings are ready, click **Generate Parts**.
2. The server will slice the model and write the files to your local drive.
3. Once finished, the parts checklist changes into individual **Download** buttons.
4. Download the `.obj` files, import them into your slicer of choice (Cura, PrusaSlicer, OrcaSlicer, or Bambu Studio), add support structures, and start printing!

---

## ⚖️ Legal Disclaimer (Gaijin EULA & Trademarks)

This software is an unofficial, community-driven open-source project. Please read the following legal notice carefully:

1. **No Affiliation**: This project is **not** affiliated, authorized, associated, sponsored, endorsed by, or in any way officially connected with Gaijin Entertainment, Gaijin Network Ltd., or any of their subsidiaries or affiliates.
2. **Intellectual Property & Trademarks**: "War Thunder", the War Thunder logo, and all related vehicle designs, names, and assets are trademarks or registered trademarks of Gaijin Entertainment or their respective manufacturers. Their use in this application is strictly for identification, description, and educational purposes.
3. **No Asset Distribution**: This repository **does not** contain, package, copy, or distribute any proprietary assets, copyright-protected files, 3D meshes, textures, or code belonging to Gaijin Entertainment. The tool runs purely as a local script that parses resources already present on the user's personal machine.
4. **User Responsibility**: Extracting, copying, or modifying game assets from the War Thunder client may violate Gaijin's End User License Agreement (EULA) or Terms of Service (ToS). The user of this software assumes all legal and technical risks associated with its execution. The developers of this tool are not responsible for any EULA violations, game bans, account suspensions, or damages resulting from the use of this software.
5. **Strictly Non-Commercial**: This tool is designed solely for personal, educational, and recreational scale modeling and 3D printing. Any commercial exploitation, resale of extracted assets, or redistribution of generated models is strictly prohibited.
6. **Third-Party Libraries & Liability**: The parsing and extraction of War Thunder's proprietary game formats (such as `.grp` resource packs and `.bin` vromfs files) are handled entirely by external, independent open-source tools: `wt-tools` (developed by the community, e.g., kotiwe) and `dagor_explorer`. This software merely acts as a high-level manager, visualizer, and coordinator of those external dependencies. Any technical bugs, data corruption, reverse-engineering liabilities, or issues regarding how those third-party scripts read and unpack game files are the sole responsibility of their respective authors. The author of this manager assumes no responsibility or liability for the behavior, logic, or legal status of these third-party libraries.
7. **No Warranty**: This tool is provided "as is", without warranty of any kind, express or implied.

---

## 📩 Contact / Hiring

Created and maintained by **Pelad0o**.
* **Gamer Tag:** `Pelad0o`
* **Contact email:** [gsebastianlopezillia@gmail.com](mailto:gsebastianlopezillia@gmail.com)

---
---

# ✈️ WT 3D Scale Model Manager (por Pelad0o) 🚜🚢

¡Bienvenido al **WT 3D Scale Model Manager**! Si eres entusiasta de las **impresoras 3D** (FDM o Resina) y del **modelismo a escala**, esta herramienta te permitirá extraer, escalar a dimensiones exactas y segmentar en piezas imprimibles cualquier vehículo (avión, tanque o barco) directamente desde tu instalación de **War Thunder**.

---

## 🛠️ Guía de Instalación para NO Programadores

No te preocupes, no necesitas saber programar ni tener Python instalado para usar esta herramienta. Sigue estos sencillos pasos:

### Paso 1: Descargar la Aplicación
1. Descarga el archivo `WT_3D_Manager.exe` de la última versión (o descomprime el `.zip` descargado).

### Paso 2: ¡A arrancar el programa!
* En Windows, simplemente haz doble clic en el archivo `WT_3D_Manager.exe`.
* **Lo que hace de forma automática:**
  * Crea tu archivo de configuración local `config.json`.
  * Intenta detectar automáticamente la ruta de tu juego War Thunder. Si no la encuentra, abrirá una ventana para que selecciones la carpeta de instalación.
  * Inicia el servidor web local y abre la aplicación en tu navegador de forma automática.
  * Si el navegador no se abre automáticamente, entra a:
     👉 **[http://localhost:8000](http://localhost:8000)**

---

## 📐 Guía de Uso para Impresión 3D y Modelismo

### ⚠️ Nota Importante: Modelos de Juego (Mallas de Renderizado) vs. Modelos Imprimibles

> [!WARNING]
> **POR FAVOR, LEE ESTO ANTES DE IMPRIMIR PARA EVITAR FRUSTACIONES:**
> Los modelos 3D extraídos del juego están diseñados originalmente para **renderizado en tiempo real** (gráficos de computadora), no para impresión 3D física.
> * **Qué significa esto:** Los modelos del juego contienen geometrías tipo "cáscara" (superficies con grosor cero, como alas, chapas o alerones), bordes no maniformes, mallas abiertas e intersecciones internas. Los laminadores (como Cura, PrusaSlicer, OrcaSlicer o Bambu Studio) necesitan volúmenes cerrados y herméticos ("watertight" o sólidos maniformes) para rebanar correctamente.
> * **El propósito de esta herramienta:** Los archivos `.obj` generados te sirven como una **base tridimensional excelente y sumamente precisa** para que no tengas que diseñar el modelo desde cero.
> * **Flujo de trabajo recomendado:** Antes de mandar las piezas al laminador, te recomendamos abrir los archivos `.obj` generados en un software de reparación o modelado 3D (como **Blender**, **Autodesk Meshmixer**, **Windows 3D Builder** o **Fusion 360**) para cerrar las mallas abiertas, darles grosor físico a las superficies delgadas (como hélices, alerones o chapas), fusionar intersecciones y realizar una reparación de malla sólida (usando herramientas como "Make Solid" o "Shrinkwrap") para dejarlas listas para una impresión exitosa.

Una vez dentro de la interfaz web, tendrás un panel visual interactivo de última generación:

### 1. Buscar y Seleccionar tu Vehículo
En la barra lateral izquierda verás una lista de vehículos detectados en tu juego. Puedes usar las pestañas de **Aviones**, **Tanques** y **Barcos** para filtrar la lista al instante, o escribir en el buscador (ej. *Bf 109*, *Sherman*, *Fletcher*). Haz clic sobre el vehículo para cargar su vista 3D interactiva.

### 2. Ajuste de Escala Física Exacta
En lugar de adivinar el tamaño en tu software laminador (Slicer), el gestor calcula las dimensiones de impresión reales:
* **Escala Proporcional Estándar (Recomendado):** Selecciona escalas de modelismo tradicionales de la lista desplegable:
  * **1:35** (La escala estándar para vehículos militares terrestres/tanques).
  * **1:32 o 1:48** (Escalas excelentes para aviones detallados).
  * **1:72** (Ideal para miniaturas de aviones o tanques rápidos de imprimir).
  * **1:100** (Perfecto para juegos de mesa).
* **Escala por Medida Objetivo:** Si quieres que tu avión tenga exactamente 30 cm (300 mm) de envergadura (ancho de alas) o tu tanque tenga 15 cm de largo, selecciona el modo correspondiente y ajusta el deslizador.

### 3. Nivel de Segmentación (¡Tu mejor aliado para imprimir!)
Los modelos 3D de los juegos vienen pegados en un solo bloque complejo con partes internas difíciles de imprimir. Esta opción divide el modelo automáticamente para facilitar la impresión y pintura:
* **Nivel 1 (Decorativo / Fusionado):** Fusiona todo el vehículo en un bloque sólido y robusto. Ideal para imprimir rápido de una sola pieza en FDM o miniaturas pequeñas en resina.
* **Nivel 2 (Estático / Semi-despiezado):** Separa las partes grandes de las pequeñas de forma lógica. Por ejemplo, en un avión mantendrá las alas y fuselaje unidos, pero separará la hélice, las ruedas del tren y la cúpula de vidrio. Ideal para pintar por separado antes de pegar.
* **Nivel 3 (Funcional / Despiece total):** Desarma por completo el vehículo en piezas individuales (flaps, alerones, timones de cola, escotillas de tanques, ruedas individuales, cañones y torretas de barcos). Es el nivel preferido para modelistas experimentados que quieren colocar ejes móviles, bisagras o electrónica.

### 4. Variantes de Daño de Batalla
Muchos vehículos tienen modelos alternativos en el juego que muestran daños. La herramienta los detecta solos y te permite elegir si quieres generar, por ejemplo, una hélice sana o doblada por un aterrizaje forzoso, o partes intactas frente a dañadas por disparos.

### 5. Vista Explotada ("Explode View")
Usa el deslizador de **Despiece** en la base del visor 3D para ver cómo se separan las piezas en el espacio. Te servirá como guía visual interactiva de ensamblaje una vez impresas las partes físicas. Puedes también marcar o desmarcar casillas en la lista de piezas para ocultar las que no te interesa imprimir (por ejemplo, si no quieres imprimir las bombas o los soportes de armas).

### 6. Generar y Descargar
1. Una vez configurada la escala y las exclusiones, haz clic en **Generar Piezas** (Generate Parts).
2. El servidor procesará y cortará el modelo en tu disco.
3. Al finalizar, la lista de piezas se transformará en botones individuales de **Descargar (Download)**.
4. Descarga los archivos `.obj`, impórtalos en tu laminador favorito (Cura, PrusaSlicer, OrcaSlicer o Bambu Studio), añade soportes si es necesario, ¡y a imprimir!

---

## ⚖️ Descargo de Responsabilidad Legal (EULA de Gaijin y Marcas)

Este software es un proyecto de código abierto no oficial desarrollado por la comunidad. Por favor, lee atentamente el siguiente aviso legal:

1. **Sin Afiliación**: Este proyecto **no** está afiliado, y no está autorizado, asociado, patrocinado, respaldado ni conectado de ninguna manera oficial con Gaijin Entertainment, Gaijin Network Ltd., ni ninguna de sus subsidiarias o filiales.
2. **Propiedad Intelectual y Marcas**: "War Thunder", el logotipo de War Thunder y todos los diseños, nombres y recursos de vehículos relacionados son marcas comerciales o registradas de Gaijin Entertainment o de sus respectivos fabricantes. Su uso en esta aplicación es estrictamente para fines de identificación, descripción y educación.
3. **Sin Distribución de Recursos**: Este repositorio **no** contiene, empaqueta, copia ni distribuye ningún recurso propietario, archivos protegidos por derechos de autor, mallas 3D, texturas o código perteneciente a Gaijin Entertainment. La herramienta funciona exclusivamente como un script local que analiza recursos que ya se encuentran presentes en la máquina personal del usuario.
4. **Responsabilidad del Usuario**: La extracción, copia o modificación de recursos del juego desde el cliente de War Thunder puede violar el Acuerdo de Licencia de Usuario Final (EULA) o los Términos de Servicio (ToS) de Gaijin. El usuario de este software asume todos los riesgos legales y técnicos asociados con su ejecución. Los desarrolladores de esta herramienta no se hacen responsables de ninguna violación del EULA, bloqueos de juego (bans), suspensiones de cuentas o daños resultantes del uso de este software.
5. **Uso Estrictamente No Comercial**: Esta herramienta está diseñada únicamente para fines de modelismo a escala e impresión 3D de carácter personal, educativo y recreativo. Queda estrictamente prohibido cualquier uso comercial, reventa de recursos extraídos o redistribución de los modelos generados.
6. **Librerías de Terceros y Responsabilidad**: La extracción y el procesamiento de los formatos propietarios de War Thunder (como archivos `.grp` y `.bin` de vromfs) son manejados en su totalidad por herramientas externas e independientes de código abierto: `wt-tools` (desarrollado por la comunidad, ej. kotiwe) y `dagor_explorer`. Este software actúa únicamente como un gestor de alto nivel, visualizador y coordinador que se comunica con esas dependencias externas. Cualquier fallo técnico, corrupción de datos, problemas derivados del análisis de binarios o responsabilidades legales sobre cómo dichas librerías externas leen y desempaquetan los archivos del juego corresponden de forma única y exclusiva a los autores de dichos proyectos. El autor de este gestor no asume ninguna responsabilidad o garantía por el comportamiento, la lógica o el estatus legal de estas librerías de terceros.
7. **Sin Garantías**: Esta herramienta se proporciona "tal cual" (as is), sin garantía de ningún tipo, expresa o implícita.

---

## 📩 Contacto / Contrataciones

Creado y mantenido por **Pelad0o**.
* **Gamer Tag:** `Pelad0o`
* **Correo electrónico de contacto:** [gsebastianlopezillia@gmail.com](mailto:gsebastianlopezillia@gmail.com)
