import os
import sys
import json
import shutil
import http.server
import socketserver
import urllib.parse
import urllib.request
import ssl
import threading
import tempfile

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Add local vendored libraries to python path
sys.path.append(resource_path(r'.\lib\dae'))
sys.path.append(resource_path(r'.\lib'))

try:
    from parse.gameres import GameResourcePack, GameResDesc
    from parse.material import DDSxTexturePack2
    from util.assetcacher import AssetCacher
    from parse.realres import DynModel
    from wt_tools.formats.vromfs_parser import vromfs_file
except ModuleNotFoundError as e:
    print("\n" + "="*80)
    print("ERROR: Missing required vendored dependencies in the 'lib/' folder.")
    print(f"Details: {e}")
    print("Please make sure the repository was cloned completely with the 'lib/' directory.")
    print("="*80 + "\n")
    sys.exit(1)
import csv

PORT = 8000

# Create a clean data directory for user files
USER_DATA_DIR = os.path.abspath(r'.\WT_3D_Exports')
os.makedirs(USER_DATA_DIR, exist_ok=True)

INDEX_FILE = os.path.join(USER_DATA_DIR, 'vehicles_index.json')
CONFIG_FILE = os.path.join(USER_DATA_DIR, 'config.json')

# Load path settings from config.json if it exists, otherwise resolve it
WT_ROOT = None
OUTPUT_ROOT = USER_DATA_DIR

def get_registry_value(key, subkey, value):
    try:
        import winreg
        reg_key = winreg.OpenKey(key, subkey)
        val, _ = winreg.QueryValueEx(reg_key, value)
        return val
    except Exception:
        return None

def detect_wt_path():
    # 1. Check registry for Gaijin launcher
    try:
        import winreg
        for key in [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]:
            for subkey in [r"Software\Gaijin\WarThunder", r"Software\Gaijin\War Thunder", r"Software\Gaijin\Launcher"]:
                for val_name in ["Path", "Location", "InstallPath"]:
                    path = get_registry_value(key, subkey, val_name)
                    if path and os.path.exists(os.path.join(path, "content")):
                        return path
    except Exception:
        pass

    # 2. Check registry for Steam installation
    try:
        import winreg
        steam_path = get_registry_value(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath")
        if steam_path:
            steam_wt = os.path.join(steam_path, "steamapps", "common", "War Thunder")
            if os.path.exists(os.path.join(steam_wt, "content")):
                return steam_wt
    except Exception:
        pass

    # 3. Check common hardcoded paths
    common_paths = [
        r"C:\Program Files (x86)\Steam\steamapps\common\War Thunder",
        r"D:\SteamLibrary\steamapps\common\War Thunder",
        r"E:\SteamLibrary\steamapps\common\War Thunder",
        r"C:\Games\War Thunder",
        r"D:\Games\War Thunder",
        r"D:\Juegos\steam\steamapps\common\War Thunder",
    ]
    for p in common_paths:
        if os.path.exists(os.path.join(p, "content")):
            return p

    return None

def prompt_wt_path():
    # Try using tkinter folder dialog (built-in)
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        
        # Show prompt info box
        messagebox.showinfo(
            "Configuración inicial", 
            "No se detectó War Thunder de forma automática.\nA continuación, selecciona la carpeta principal donde tienes instalado el juego (donde está launcher.exe)."
        )
        
        folder = filedialog.askdirectory(title="Selecciona la carpeta principal de War Thunder (donde está launcher.exe)")
        root.destroy()
        if folder:
            folder = os.path.normpath(folder)
            if os.path.exists(os.path.join(folder, "content")):
                return folder
            else:
                # Error popup
                root_err = tk.Tk()
                root_err.withdraw()
                messagebox.showerror(
                    "Carpeta Incorrecta", 
                    "La carpeta seleccionada no es válida (debe contener la subcarpeta 'content')."
                )
                root_err.destroy()
    except Exception:
        pass
        
    # Fallback to console input
    while True:
        print("\n" + "="*80)
        print("CONFIGURACIÓN DE RUTA DE WAR THUNDER")
        print("="*80)
        path = input("Introduce la ruta completa de la carpeta de War Thunder (o escribe 'exit' para salir): ").strip()
        if not path or path.lower() == 'exit':
            return None
        path = os.path.normpath(path)
        if os.path.exists(os.path.join(path, "content")):
            return path
        print("Error: La ruta especificada no parece contener War Thunder (falta la carpeta 'content').")

# Load existing config or initialize
config_loaded = False
if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
            wt_root_cand = user_config.get("wt_root") or user_config.get("WT_ROOT")
            if wt_root_cand and os.path.exists(os.path.join(wt_root_cand, "content")):
                WT_ROOT = wt_root_cand
                config_loaded = True
                if "output_root" in user_config: OUTPUT_ROOT = os.path.abspath(user_config["output_root"])
                elif "OUTPUT_ROOT" in user_config: OUTPUT_ROOT = os.path.abspath(user_config["OUTPUT_ROOT"])
    except Exception as e:
        print(f"Error loading config.json: {e}")

if not config_loaded:
    # Attempt auto detection
    detected = detect_wt_path()
    if detected:
        WT_ROOT = detected
        print(f"War Thunder detectado automáticamente en: {WT_ROOT}")
    else:
        # Prompt user
        WT_ROOT = prompt_wt_path()
        if not WT_ROOT:
            print("Configuración cancelada. Saliendo...")
            sys.exit(1)
            
    # Save new config
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                "wt_root": WT_ROOT,
                "output_root": USER_DATA_DIR
            }, f, indent=4)
        print("Configuración inicial guardada en config.json")
    except Exception as e:
        print(f"Error escribiendo config.json: {e}")

# Global state
indexing_status = {
    "indexing": False,
    "progress": 0,
    "total": 0,
    "count": 0
}
vehicle_index = {}

# Keep-Alive Heartbeat variables for auto-shutdown
last_ping_time = None
ping_received = False

# Caching systems
grp_cache = {}
CACHE_DIR = os.path.join(OUTPUT_ROOT, 'model_cache')

# Clear old cache to force metadata regeneration using updated filters
if os.path.exists(CACHE_DIR):
    try:
        shutil.rmtree(CACHE_DIR)
        print("Cleared model cache successfully on startup.")
    except Exception as e:
        print(f"Warning: Failed to clear cache directory: {e}")
os.makedirs(CACHE_DIR, exist_ok=True)

def get_grp(grp_path):
    resolved_path = grp_path
    if not os.path.exists(grp_path):
        # Reconstruct path relative to WT_ROOT by searching for 'content'
        norm_path = os.path.normpath(grp_path)
        parts = norm_path.split(os.sep)
        if 'content' in parts:
            content_idx = parts.index('content')
            rel_path = os.sep.join(parts[content_idx:])
            candidate = os.path.join(WT_ROOT, rel_path)
            if os.path.exists(candidate):
                resolved_path = candidate
        else:
            candidate = os.path.join(WT_ROOT, grp_path)
            if os.path.exists(candidate):
                resolved_path = candidate

    if resolved_path not in grp_cache:
        print(f"Opening GRP archive (cold load): {resolved_path} (original requested: {grp_path})")
        grp_cache[resolved_path] = GameResourcePack(resolved_path)
    return grp_cache[resolved_path]

def get_cached_model_details(model_name):
    obj_cache_path = os.path.join(CACHE_DIR, f"{model_name}.obj")
    meta_cache_path = os.path.join(CACHE_DIR, f"{model_name}_metadata.json")
    
    if os.path.exists(obj_cache_path) and os.path.exists(meta_cache_path):
        try:
            with open(meta_cache_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            return metadata, obj_cache_path
        except Exception as e:
            print(f"Error loading cached model metadata for {model_name}: {e}")
    return None, None

def save_model_to_cache(model_name, raw_obj_path, metadata):
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        obj_cache_path = os.path.join(CACHE_DIR, f"{model_name}.obj")
        meta_cache_path = os.path.join(CACHE_DIR, f"{model_name}_metadata.json")
        
        shutil.copy(raw_obj_path, obj_cache_path)
        with open(meta_cache_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4)
        print(f"Successfully cached model {model_name} on disk.")
    except Exception as e:
        print(f"Error writing cached model {model_name}: {e}")

def load_friendly_names():
    friendly_names = {}
    lang_path = os.path.join(WT_ROOT, 'lang.vromfs.bin')
    
    # Check root first, then look under cache folder
    if not os.path.exists(lang_path):
        cache_root = os.path.join(WT_ROOT, 'cache')
        if os.path.exists(cache_root):
            for r, d, f in os.walk(cache_root):
                if 'lang.vromfs.bin' in f:
                    lang_path = os.path.join(r, 'lang.vromfs.bin')
                    break
                    
    if os.path.exists(lang_path):
        try:
            print(f"Loading translations from {lang_path}...")
            with open(lang_path, 'rb') as f:
                data = f.read()
            parsed = vromfs_file.parse(data)
            
            for i in range(parsed.body.data.data.files_count):
                filename = parsed.body.data.data.filename_table.filenames[i].filename
                if filename == 'lang/units.csv':
                    csv_data = parsed.body.data.data.file_data_table.file_data_list[i].data
                    csv_text = csv_data.decode('utf-8', errors='ignore')
                    
                    reader = csv.reader(csv_text.splitlines(), delimiter=';')
                    for row in reader:
                        if len(row) > 5:
                            row_id = row[0].strip('"')
                            english_name = row[1].strip('"')
                            spanish_name = row[5].strip('"')
                            
                            friendly = spanish_name if spanish_name else english_name
                            if friendly:
                                friendly_names[row_id] = friendly
                    break
            print(f"Successfully loaded {len(friendly_names)} translation keys.")
        except Exception as e:
            print(f"Error parsing translations from vromfs: {e}")
    else:
        print(f"Translations file not found at {lang_path}")
            
    return friendly_names

def get_friendly_name(vname, translations):
    candidates = []
    
    # 1. Base candidates
    for base in [vname, vname.replace('_', '-'), vname.replace('_', '-', 1), vname.replace('_', '-', 2)]:
        candidates.extend([f"{base}_shop", f"{base}_0", f"{base}_1", base])
        
    # 2. Check prefix versions
    prefixes = ["germ_", "ussr_", "us_", "jp_", "it_", "fr_", "uk_", "cn_", "sw_"]
    for pref in prefixes:
        if vname.startswith(pref):
            short_name = vname[len(pref):]
            for base in [short_name, short_name.replace('_', '-'), short_name.replace('_', '-', 1), short_name.replace('_', '-', 2)]:
                candidates.extend([f"{base}_shop", f"{base}_0", f"{base}_1", base])
            break
            
    seen = set()
    deduped_candidates = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            deduped_candidates.append(c)
            
    for cand in deduped_candidates:
        if cand in translations:
            val = translations[cand].strip()
            # Clean symbols like special characters (▄, ▅, ▃, ◔, , ◗)
            for sym in ["▄", "▅", "▃", "◔", "", "◗", ""]:
                val = val.replace(sym, "")
            # Replace non-breaking spaces with standard spaces
            val = val.replace('\u00a0', ' ').replace('\xa0', ' ')
            val = val.strip()
            if val:
                return val
                
    # Fallback to cleaning the technical name using Regex
    import re
    # 1. Remove technical suffixes
    name = re.sub(r'_(shop|early|late|premium|tutorial|mod|rocket|space|naval|football)$', '', vname, flags=re.IGNORECASE)
    
    # 2. Add dashes to Letter_Number combos (f_4e -> f-4e, p_51 -> p-51)
    name = re.sub(r'(^|_)([a-zA-Z]{1,4})_(\d+[a-zA-Z]*)(?=_|$)', r'\1\2-\3', name)
    name = re.sub(r'(^|_)([a-zA-Z]{1,4}-\d+[a-zA-Z]*)_(\d+[a-zA-Z]*)(?=_|$)', r'\1\2-\3', name)
    
    # 3. Format common prefixes (pz_iv -> pz.iv)
    name = re.sub(r'(^|_)pz_([ivx]+)(?=_|$)', r'\1pz.\2', name)
    name = re.sub(r'(^|_)bf_109(?=_|$)', r'\1bf-109', name)
    
    # 4. Title case while keeping lower case for small words
    clean_parts = []
    for p in name.split('_'):
        p_lower = p.lower()
        if p_lower in ['of', 'the', 'de', 'del', 'ausf', 'mk', 'mod']:
            if p_lower == 'ausf': clean_parts.append('Ausf.')
            elif p_lower == 'mk': clean_parts.append('Mk.')
            elif p_lower == 'mod': clean_parts.append('Mod.')
            else: clean_parts.append(p_lower)
        else:
            clean_parts.append(p.title())
            
    res = " ".join(clean_parts)
    # Roman numeral fix
    res = re.sub(r'\b(Ii|Iii|Iv|Vi|Vii|Viii|Ix|Xi)\b', lambda m: m.group(1).upper(), res)
    return res

def scan_vehicles_thread():
    global vehicle_index, indexing_status
    indexing_status["indexing"] = True
    indexing_status["count"] = 0
    
    print("Background indexing started...")
    
    # Check cache first
    if os.path.exists(INDEX_FILE):
        try:
            with open(INDEX_FILE, 'r') as f:
                vehicle_index = json.load(f)
                
            # Check if we have ships in cache. If not, re-index.
            has_ships = any(v.get("category") == "ship" for v in vehicle_index.values())
            
            if has_ships:
                # Load translations
                translations = load_friendly_names()
                
                # Inject friendly names if missing or outdated
                updated = False
                for name, v in vehicle_index.items():
                    if "friendly_name" not in v or not v["friendly_name"] or v["friendly_name"] == v["name"]:
                        v["friendly_name"] = get_friendly_name(name, translations)
                        updated = True
                        
                if updated:
                    with open(INDEX_FILE, 'w') as f:
                        json.dump(vehicle_index, f, indent=4)
                        
                indexing_status["indexing"] = False
                print(f"Loaded {len(vehicle_index)} vehicles from cache with friendly names.")
                return
            else:
                print("Cache found but missing ships. Forcing full scan to index naval units...")
                vehicle_index = {}
        except Exception as e:
            print(f"Error loading index cache: {e}")
            
    folders = [
        ('aircraft', os.path.join(WT_ROOT, r'content\base\res\aircrafts')),
        ('tank', os.path.join(WT_ROOT, r'content\base\res\tanks')),
        ('ship', os.path.join(WT_ROOT, r'content\base\res\ships'))
    ]
    
    # First count total GRP files
    grp_paths = []
    for cat, folder in folders:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                if file.endswith('.grp'):
                    grp_paths.append((cat, os.path.join(folder, file)))
                    
    indexing_status["total"] = len(grp_paths)
    
    # Load translations for new indexing
    translations = load_friendly_names()
    
    for i, (cat, path) in enumerate(grp_paths):
        indexing_status["progress"] = i + 1
        try:
            # GameResourcePack only parses the metadata table, very fast
            grp = GameResourcePack(path)
            for j in range(grp.getRealResEntryCnt()):
                entry = grp.getRealResEntry(j)
                name = entry.getName()
                
                # Check classId for DynModel (0xb4b7d9c4)
                # entry.getRealResData() is fast as it doesn't parse vertices
                res_data = entry.getRealResData()
                if isinstance(res_data, DynModel):
                    vehicle_index[name] = {
                        "name": name,
                        "friendly_name": get_friendly_name(name, translations),
                        "grp_path": path,
                        "category": cat,
                        "res_index": j
                    }
                    indexing_status["count"] += 1
        except Exception:
            pass
            
    # Save cache
    try:
        with open(INDEX_FILE, 'w') as f:
            json.dump(vehicle_index, f, indent=4)
    except Exception as e:
        print(f"Failed to save index cache: {e}")
        
    indexing_status["indexing"] = False
    print(f"Background indexing completed. Found {len(vehicle_index)} dynamic models.")

# Lock to serialize model extraction (prevents concurrent temp_export conflicts)
_model_extract_lock = threading.Lock()

def get_temp_raw_model(model_name, grp_path):
    # Load and cache skeletons in this GRP using cached GRP loader
    grp = get_grp(grp_path)
    for i in range(grp.getRealResEntryCnt()):
        entry = grp.getRealResEntry(i)
        if entry.getName().endswith('_skeleton'):
            try:
                skeleton_res = grp.getRealResource(i)
                AssetCacher.cacheAsset(skeleton_res)
            except Exception:
                pass
                
    # Get model and export it to a unique temp dir
    res_id = grp.getRealResId(model_name)
    dyn_model = grp.getRealResource(res_id)
    dyn_model.computeData()
    
    mdl = dyn_model.getModel(0)
    mdl._Model__exportName = model_name
    
    temp_dir = tempfile.mkdtemp(prefix=f"wt_{model_name}_", dir=os.path.abspath('.'))
    
    mdl.exportObj(temp_dir, exportTexture=False)
    
    raw_obj_path = os.path.join(temp_dir, f"{model_name}.obj")
    return raw_obj_path, temp_dir

def parse_obj_metadata(raw_obj_path):
    vertices = []
    groups = []
    current_group = None
    
    if not os.path.exists(raw_obj_path):
        return None
        
    seen_groups = set()
    with open(raw_obj_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.split()
                vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
            elif line.startswith('g '):
                current_group = line[2:].strip()
                if current_group not in seen_groups:
                    groups.append(current_group)
                    seen_groups.add(current_group)
                    
    # Exclude flare, fire, and blur groups
    exclude_keywords = ['flare', 'fire', 'prop_side', 'prop_wind', 'Object001']
    filtered_groups = [g for g in groups if not any(k in g.lower() for k in exclude_keywords)]
    
    if not vertices:
        return {"length": 0, "height": 0, "wingspan": 0, "groups": []}
        
    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    zs = [v[2] for v in vertices]
    
    return {
        "length": max(xs) - min(xs),
        "height": max(ys) - min(ys),
        "wingspan": max(zs) - min(zs),
        "groups": filtered_groups
    }

def classify_groups(raw_groups, level, category):
    groups_map = {}
    if level == 1:
        # Level 1: Modelo homogéneo (100% en un solo grupo)
        groups_map['body'] = list(raw_groups)
        
    elif level == 2:
        if category == 'tank':
            # Level 2: Tanks moving/functional parts
            turret_groups = []
            barrel_groups = []
            track_left = []
            track_right = []
            wheels_left = []
            wheels_right = []
            hatch_groups = []
            weapons_groups = []
            launchers_groups = []
            payload_groups = []
            body_groups = []
            
            for g in raw_groups:
                gl = g.lower()
                if 'turret' in gl:
                    turret_groups.append(g)
                elif any(b in gl for b in ['gun_barrel', 'barrel', 'cannon']) and not any(mg in gl for mg in ['mg', 'mgun']):
                    barrel_groups.append(g)
                elif 'track' in gl:
                    if any(l in gl for l in ['_l', 'l_', 'left']):
                        track_left.append(g)
                    else:
                        track_right.append(g)
                elif any(w in gl for w in ['wheel', 'roller', 'sprocket', 'idler', 'suspension']):
                    if any(l in gl for l in ['_l', 'l_', 'left']):
                        wheels_left.append(g)
                    else:
                        wheels_right.append(g)
                elif any(h in gl for h in ['hatch', 'door', 'cover']):
                    hatch_groups.append(g)
                elif any(arm in gl for arm in ['pylon', 'launcher', 'rack', 'pod', 'tube']):
                    launchers_groups.append(g)
                elif any(arm in gl for arm in ['mg', 'mgun', 'machinegun', 'flak']):
                    weapons_groups.append(g)
                elif any(arm in gl for arm in ['bomb', 'rocket', 'missile', 'torpedo']):
                    payload_groups.append(g)
                else:
                    body_groups.append(g)
                    
            if body_groups: groups_map['body'] = body_groups
            if turret_groups: groups_map['turret'] = turret_groups
            if barrel_groups: groups_map['barrel'] = barrel_groups
            if track_left: groups_map['track_left'] = track_left
            if track_right: groups_map['track_right'] = track_right
            if wheels_left: groups_map['wheels_left'] = wheels_left
            if wheels_right: groups_map['wheels_right'] = wheels_right
            if hatch_groups: groups_map['hatches'] = hatch_groups
            if weapons_groups: groups_map['weapons'] = weapons_groups
            if launchers_groups: groups_map['launchers'] = launchers_groups
            if payload_groups: groups_map['payload'] = payload_groups

        elif category == 'ship':
            # Level 2: Ships moving/functional parts
            turrets = []
            guns = []
            propeller = []
            rudder = []
            radars = []
            weapons_groups = []
            launchers_groups = []
            payload_groups = []
            body_groups = []
            
            for g in raw_groups:
                gl = g.lower()
                if 'turret' in gl:
                    turrets.append(g)
                elif any(b in gl for b in ['gun', 'barrel', 'cannon']) and not any(mg in gl for mg in ['mg', 'mgun']):
                    guns.append(g)
                elif any(p in gl for p in ['prop', 'screw']):
                    propeller.append(g)
                elif 'rudder' in gl:
                    rudder.append(g)
                elif any(r in gl for r in ['radar', 'crane', 'director']):
                    radars.append(g)
                elif any(arm in gl for arm in ['launcher', 'torpedo_tube', 'rack', 'pod', 'tube']):
                    launchers_groups.append(g)
                elif any(arm in gl for arm in ['mg', 'mgun', 'flak', 'depth_charge_mount']):
                    weapons_groups.append(g)
                elif any(arm in gl for arm in ['torpedo', 'rocket', 'depth_charge']):
                    payload_groups.append(g)
                else:
                    body_groups.append(g)
                    
            if body_groups: groups_map['body'] = body_groups
            if turrets: groups_map['turrets'] = turrets
            if guns: groups_map['guns'] = guns
            if propeller: groups_map['propeller'] = propeller
            if rudder: groups_map['rudder'] = rudder
            if radars: groups_map['radars'] = radars
            if weapons_groups: groups_map['weapons'] = weapons_groups
            if launchers_groups: groups_map['launchers'] = launchers_groups
            if payload_groups: groups_map['payload'] = payload_groups

        else: # aircraft / other
            # Level 2: Aircraft moving/functional parts
            body_groups = []
            wing_l_control = []
            wing_r_control = []
            rudder_groups = []
            elev_l_groups = []
            elev_r_groups = []
            propeller_groups = []
            canopy_groups = []
            gear_left = []
            gear_right = []
            gear_tail = []
            weapons_groups = []
            launchers_groups = []
            payload_groups = []
            
            for g in raw_groups:
                gl = g.lower()
                if any(p in gl for p in ['prop', 'spinner']):
                    propeller_groups.append(g)
                elif any(c in gl for c in ['blister', 'canopy', 'glass']):
                    canopy_groups.append(g)
                elif 'wheel_l' in gl or 'gear_l' in gl:
                    gear_left.append(g)
                elif 'wheel_r' in gl or 'gear_r' in gl:
                    gear_right.append(g)
                elif 'wheel_c' in gl or 'gear_c' in gl:
                    gear_tail.append(g)
                elif 'rudder' in gl:
                    rudder_groups.append(g)
                elif 'elevator0' in gl or 'elevator_l' in gl:
                    elev_l_groups.append(g)
                elif 'elevator1' in gl or 'elevator_r' in gl:
                    elev_r_groups.append(g)
                elif any(w in gl for w in ['flap_l', 'flap1_l', 'flap2_l', 'aileron_l', 'slat_l']):
                    wing_l_control.append(g)
                elif any(w in gl for w in ['flap_r', 'flap1_r', 'flap2_r', 'aileron_r', 'slat_r']):
                    wing_r_control.append(g)
                elif any(arm in gl for arm in ['pylon', 'launcher', 'rack', 'pod', 'tube']) and 'track' not in gl:
                    launchers_groups.append(g)
                elif any(arm in gl for arm in ['gun', 'mg', 'cannon', 'mgun', 'aa_gun', 'flak']):
                    weapons_groups.append(g)
                elif any(arm in gl for arm in ['bomb', 'rocket', 'missile', 'torpedo', '210mm']):
                    payload_groups.append(g)
                else:
                    body_groups.append(g)
                    
            if body_groups: groups_map['body'] = body_groups
            if propeller_groups: groups_map['propeller'] = propeller_groups
            if canopy_groups: groups_map['canopy'] = canopy_groups
            if gear_left: groups_map['landing_gear_left'] = gear_left
            if gear_right: groups_map['landing_gear_right'] = gear_right
            if gear_tail: groups_map['landing_gear_tail'] = gear_tail
            if rudder_groups: groups_map['rudder'] = rudder_groups
            if elev_l_groups: groups_map['elevator_left'] = elev_l_groups
            if elev_r_groups: groups_map['elevator_right'] = elev_r_groups
            if wing_l_control: groups_map['wing_left_control_surfaces'] = wing_l_control
            if wing_r_control: groups_map['wing_right_control_surfaces'] = wing_r_control
            if weapons_groups: groups_map['weapons'] = weapons_groups
            if launchers_groups: groups_map['launchers'] = launchers_groups
            if payload_groups: groups_map['payload'] = payload_groups
        
    else:
        # Level 3: Funcional (Máxima Segmentación)
        for g in raw_groups:
            clean_name = g.replace(' ', '_').replace(':', '_')
            if clean_name not in groups_map:
                groups_map[clean_name] = []
            groups_map[clean_name].append(g)
            
    return groups_map

def run_segmentation_pipeline(raw_obj_path, target_dir, groups_map, scale_factor):
    exclude_groups = {
        'flare1', 'flare2', 'flare3', 'flare4', 'flare5', 'flare6', 'flare7', 'flare8', 'flare9', 'flare10',
        'fire1_1', 'fire1_2', 'fire1_3', 'fire1_4', 'fire1_5', 'fire1_6', 'fire1_7', 'fire1_8', 'fire1_9', 'fire1_10', 'fire1_11', 'fire1_12',
        'prop02_1', 'prop03_1', 'prop_side_1', 'prop01_1_dmg', 'Object001'
    }
    
    vertices = []
    uvs = []
    normals = []
    group_faces = {}
    current_group = None
    current_material = None
    
    with open(raw_obj_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.split()
                vertices.append((float(parts[1]) * scale_factor, float(parts[2]) * scale_factor, float(parts[3]) * scale_factor))
            elif line.startswith('vt '):
                parts = line.strip().split()
                uvs.append((float(parts[1]), float(parts[2])))
            elif line.startswith('vn '):
                parts = line.strip().split()
                normals.append((float(parts[1]), float(parts[2]), float(parts[3])))
            elif line.startswith('g '):
                current_group = line.strip()[2:]
                group_faces[current_group] = []
            elif line.startswith('usemtl '):
                current_material = line.strip()[7:]
            elif line.startswith('f '):
                if current_group:
                    parts = line.strip().split()[1:]
                    face_verts = []
                    for p in parts:
                        indices = p.split('/')
                        v_idx = int(indices[0]) - 1
                        vt_idx = int(indices[1]) - 1 if len(indices) > 1 and indices[1] else -1
                        vn_idx = int(indices[2]) - 1 if len(indices) > 2 and indices[2] else -1
                        face_verts.append((v_idx, vt_idx, vn_idx))
                    group_faces[current_group].append((face_verts, current_material))
                    
    generated_files = []
    for filename, target_groups in groups_map.items():
        file_group_faces = {g: group_faces[g] for g in target_groups if g in group_faces}
        total_faces = sum(len(faces) for faces in file_group_faces.values())
        if total_faces == 0:
            continue
            
        sub_v_map = {}
        sub_vt_map = {}
        sub_vn_map = {}
        sub_vertices = []
        sub_uvs = []
        sub_normals = []
        
        for g, faces in file_group_faces.items():
            for face_verts, mat in faces:
                for v_idx, vt_idx, vn_idx in face_verts:
                    if v_idx not in sub_v_map:
                        sub_v_map[v_idx] = len(sub_vertices)
                        sub_vertices.append(vertices[v_idx])
                    if vt_idx != -1 and vt_idx not in sub_vt_map:
                        sub_vt_map[vt_idx] = len(sub_uvs)
                        sub_uvs.append(uvs[vt_idx])
                    if vn_idx != -1 and vn_idx not in sub_vn_map:
                        sub_vn_map[vn_idx] = len(sub_normals)
                        sub_normals.append(normals[vn_idx])
                        
        sub_out_path = os.path.join(target_dir, f"{filename}.obj")
        
        with open(sub_out_path, 'w') as f:
            f.write("# Exported by WT Scale Model Manager\n")
            for v in sub_vertices:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            for vt in sub_uvs:
                f.write(f"vt {vt[0]:.4f} {vt[1]:.4f}\n")
            for vn in sub_normals:
                f.write(f"vn {vn[0]:.4f} {vn[1]:.4f} {vn[2]:.4f}\n")
                
            for g, faces in file_group_faces.items():
                f.write(f"g {g}\n")
                last_mat = None
                for face_verts, mat in faces:
                    if mat != last_mat:
                        f.write(f"usemtl {mat}\n")
                        last_mat = mat
                    
                    f_parts = []
                    for v_idx, vt_idx, vn_idx in face_verts:
                        new_v = sub_v_map[v_idx] + 1
                        new_vt = sub_vt_map[vt_idx] + 1 if vt_idx != -1 else ""
                        new_vn = sub_vn_map[vn_idx] + 1 if vn_idx != -1 else ""
                        f_parts.append(f"{new_v}/{new_vt}/{new_vn}")
                    f.write(f"f {' '.join(f_parts)}\n")
                    
        generated_files.append(f"{filename}.obj")
        
    return generated_files

class WebManagerHandler(http.server.SimpleHTTPRequestHandler):
    def handle(self):
        """Override handle to catch broken pipe errors when browser disconnects (e.g. refresh)."""
        try:
            super().handle()
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError) as e:
            # Client disconnected mid-response (browser refresh, tab close, etc.)
            # This is normal and should not crash the server thread.
            pass

    def log_message(self, format, *args):
        """Suppress noisy default HTTP logging for thumbnails."""
        msg = format % args
        if '/api/thumbnail' not in msg and '/api/ping' not in msg:
            super().log_message(format, *args)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def send_response_compressed(self, content_bytes, content_type, cache_control=None):
        import gzip
        accept_encoding = self.headers.get('Accept-Encoding', '')
        should_compress = 'gzip' in accept_encoding and len(content_bytes) > 1024
        
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        if cache_control:
            self.send_header('Cache-Control', cache_control)
            
        if should_compress:
            self.send_header('Content-Encoding', 'gzip')
            compressed = gzip.compress(content_bytes)
            self.send_header('Content-Length', str(len(compressed)))
            self.end_headers()
            self.wfile.write(compressed)
        else:
            self.send_header('Content-Length', str(len(content_bytes)))
            self.end_headers()
            self.wfile.write(content_bytes)

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = urllib.parse.parse_qs(parsed_url.query)
        
        if path == '/api/ping':
            global last_ping_time, ping_received
            import time
            last_ping_time = time.time()
            ping_received = True
            self.send_response_compressed(json.dumps({"status": "ok"}).encode('utf-8'), 'application/json', 'no-cache')
            return
            
        if path == '/api/vehicles':
            response = {
                "indexing": indexing_status["indexing"],
                "progress": indexing_status["progress"],
                "total": indexing_status["total"],
                "count": indexing_status["count"],
                "vehicles": list(vehicle_index.values())
            }
            content_bytes = json.dumps(response).encode('utf-8')
            self.send_response_compressed(content_bytes, 'application/json', 'no-cache')
            
        elif path == '/api/thumbnail':
            name = query.get('name', [''])[0]
            if not name:
                self.send_error(400, "Missing name parameter")
                return
                
            name = os.path.basename(name)
            if not name.endswith('.png'):
                name += '.png'
                
            thumb_dir_external = os.path.join(OUTPUT_ROOT, 'thumbnails')
            os.makedirs(thumb_dir_external, exist_ok=True)
            local_path = os.path.join(thumb_dir_external, name)
            bundled_path = resource_path(os.path.join('thumbnails', name))
            
            # Check bundled first (from PyInstaller .exe), then external
            file_to_read = None
            if os.path.exists(bundled_path):
                file_to_read = bundled_path
            elif os.path.exists(local_path):
                file_to_read = local_path
                
            if file_to_read:
                try:
                    file_size = os.path.getsize(file_to_read)
                    if file_size == 0:
                        # Negative cache: thumbnail doesn't exist in datamine, serve empty instantly
                        self.send_response_compressed(b'', 'image/png', 'public, max-age=86400')
                        return
                    with open(file_to_read, 'rb') as f:
                        content_bytes = f.read()
                    self.send_response_compressed(content_bytes, 'image/png', 'public, max-age=86400')
                    return
                except Exception as e:
                    print(f"Error reading cached thumbnail {name}: {e}")
                    
            url = f"https://raw.githubusercontent.com/gszabi99/War-Thunder-Datamine/master/atlases.vromfs.bin_u/units/{name}"
            
            def fetch_thumb(fetch_url, fetch_local):
                context = ssl._create_unverified_context()
                req = urllib.request.Request(fetch_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, context=context, timeout=5) as response:
                    c_bytes = response.read()
                with open(fetch_local, 'wb') as f:
                    f.write(c_bytes)
                return c_bytes

            try:
                content_bytes = fetch_thumb(url, local_path)
                self.send_response_compressed(content_bytes, 'image/png', 'public, max-age=86400')
            except urllib.error.HTTPError as e:
                # If 404, try regex fallback name to increase hit rate
                if e.code == 404:
                    import re
                    clean_name = re.sub(r'_(shop|early|late|premium|tutorial)$', '', name.replace('.png', ''))
                    if clean_name != name.replace('.png', ''):
                        fallback_url = f"https://raw.githubusercontent.com/gszabi99/War-Thunder-Datamine/master/atlases.vromfs.bin_u/units/{clean_name}.png"
                        try:
                            content_bytes = fetch_thumb(fallback_url, local_path)
                            self.send_response_compressed(content_bytes, 'image/png', 'public, max-age=86400')
                            return
                        except urllib.error.HTTPError as fallback_e:
                            if fallback_e.code != 404:
                                print(f"Error fetching fallback thumbnail {clean_name}: {fallback_e}")
                    # Silent 404, don't spam console
                else:
                    print(f"Error fetching thumbnail {name} from datamine: {e}")
                
                # Cache negative result as an empty file
                try:
                    with open(local_path, 'wb') as f:
                        pass
                except Exception as cache_err:
                    print(f"Failed to cache empty thumbnail for {name}: {cache_err}")
                
                self.send_response_compressed(b'', 'image/png', 'public, max-age=86400')
            except Exception as e:
                print(f"Error fetching thumbnail {name} from datamine: {e}")
                try:
                    with open(local_path, 'wb') as f:
                        pass
                except Exception:
                    pass
                self.send_response_compressed(b'', 'image/png', 'public, max-age=86400')
            
        elif path == '/api/details':
            model = query.get('model', [''])[0]
            grp = query.get('grp', [''])[0]
            
            if not model or not grp:
                self.send_error(400, "Missing model or grp parameters")
                return
                
            try:
                # Try cache first!
                metadata, cached_obj_path = get_cached_model_details(model)
                if metadata and cached_obj_path:
                    print(f"Serving {model} details from cache.")
                    content_bytes = json.dumps(metadata).encode('utf-8')
                    self.send_response_compressed(content_bytes, 'application/json', 'private, max-age=3600')
                    return
                
                # If cache miss, extract with lock to prevent concurrent temp conflicts
                with _model_extract_lock:
                    # Re-check cache after acquiring lock (another thread may have populated it)
                    metadata, cached_obj_path = get_cached_model_details(model)
                    if metadata and cached_obj_path:
                        content_bytes = json.dumps(metadata).encode('utf-8')
                        self.send_response_compressed(content_bytes, 'application/json', 'private, max-age=3600')
                        return
                    
                    raw_obj, temp_dir = get_temp_raw_model(model, grp)
                    metadata = parse_obj_metadata(raw_obj)
                    
                    # Save to cache
                    save_model_to_cache(model, raw_obj, metadata)
                    
                    if temp_dir and os.path.exists(temp_dir):
                        try:
                            shutil.rmtree(temp_dir)
                        except OSError:
                            pass  # will be cleaned up later
                
                content_bytes = json.dumps(metadata).encode('utf-8')
                self.send_response_compressed(content_bytes, 'application/json', 'private, max-age=3600')
            except Exception as e:
                self.send_response_compressed(json.dumps({"error": str(e)}).encode('utf-8'), 'application/json')
                
        elif path == '/api/model':
            model = query.get('model', [''])[0]
            grp = query.get('grp', [''])[0]
            
            if not model:
                self.send_error(400, "Missing model parameter")
                return
                
            try:
                # Try cache first!
                metadata, cached_obj_path = get_cached_model_details(model)
                if not cached_obj_path or not os.path.exists(cached_obj_path):
                    if not grp:
                        self.send_error(400, "Missing grp parameter for extraction")
                        return
                    # Extraction (cache miss) - use lock
                    with _model_extract_lock:
                        # Re-check cache after acquiring lock
                        metadata, cached_obj_path = get_cached_model_details(model)
                        if not cached_obj_path or not os.path.exists(cached_obj_path):
                            raw_obj, temp_dir = get_temp_raw_model(model, grp)
                            metadata = parse_obj_metadata(raw_obj)
                            save_model_to_cache(model, raw_obj, metadata)
                            cached_obj_path = os.path.join(CACHE_DIR, f"{model}.obj")
                            if temp_dir and os.path.exists(temp_dir):
                                try:
                                    shutil.rmtree(temp_dir)
                                except OSError:
                                    pass
                
                # Serve the cached obj file directly
                with open(cached_obj_path, 'rb') as f:
                    content_bytes = f.read()
                
                self.send_response_compressed(content_bytes, 'application/octet-stream', 'private, max-age=3600')
            except Exception as e:
                self.send_error(500, f"Error loading model: {e}")
                
        elif path == '/preview_model.obj':
            target_path = os.path.join(OUTPUT_ROOT, 'preview_model.obj')
            if os.path.exists(target_path):
                with open(target_path, 'rb') as f:
                    content_bytes = f.read()
                self.send_response_compressed(content_bytes, 'application/octet-stream', 'private, max-age=3600')
            else:
                self.send_error(404, "Preview model not found")
                
        elif path.startswith('/parts/'):
            # Serve files from output directory, allowing subdirectories
            rel_file = path[7:] # remove /parts/
            rel_file = urllib.parse.unquote(rel_file).replace('\\', '/')
            if '..' in rel_file or rel_file.startswith('/'):
                self.send_error(400, "Invalid path")
                return
                
            target_path = os.path.normpath(os.path.join(OUTPUT_ROOT, 'split_parts', rel_file))
            if not target_path.startswith(os.path.normpath(os.path.join(OUTPUT_ROOT, 'split_parts'))):
                self.send_error(403, "Access Denied")
                return
                
            if os.path.exists(target_path) and os.path.isfile(target_path):
                with open(target_path, 'rb') as f:
                    content_bytes = f.read()
                self.send_response_compressed(content_bytes, 'application/octet-stream', 'no-cache')
            else:
                self.send_error(404, "Part file not found")
                
        else:
            # Serve index.html or styles
            if path == '/' or path == '/index.html':
                with open(resource_path('frontend/index.html'), 'rb') as f:
                    content_bytes = f.read()
                self.send_response_compressed(content_bytes, 'text/html', 'no-cache')
            elif path == '/style.css':
                with open(resource_path('frontend/style.css'), 'rb') as f:
                    content_bytes = f.read()
                self.send_response_compressed(content_bytes, 'text/css', 'no-cache')
            else:
                super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        if path == '/api/generate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = json.loads(post_data)
            
            model = params.get('model')
            grp = params.get('grp')
            scale_mode = params.get('scale_mode') # 'wingspan' or 'length' or 'multiplier'
            scale_value = float(params.get('scale_value', 1.0))
            level = int(params.get('level', 3)) # 1, 2, or 3
            conflict_action = params.get('conflict_action') # None, 'overwrite', 'version'
            
            if not model or not grp:
                self.send_error(400, "Missing model or grp parameters")
                return
                
            try:
                # 1. Determine date string and subfolder name
                from datetime import datetime
                date_str = datetime.now().strftime('%Y-%m-%d')
                folder_base = f"{model}_lvl{level}_{date_str}"
                
                # Check for existence and handle conflicts
                split_parts_root = os.path.join(OUTPUT_ROOT, 'split_parts')
                os.makedirs(split_parts_root, exist_ok=True)
                
                folder_name = folder_base
                target_dir = os.path.join(split_parts_root, folder_name)
                
                if os.path.exists(target_dir):
                    if conflict_action is None:
                        # Return conflict status
                        self.send_response_compressed(json.dumps({
                            "status": "conflict",
                            "folder_name": folder_name
                        }).encode('utf-8'), 'application/json')
                        return
                    elif conflict_action == 'overwrite':
                        shutil.rmtree(target_dir)
                        os.makedirs(target_dir, exist_ok=True)
                    elif conflict_action == 'version':
                        version = 2
                        while True:
                            folder_name = f"{folder_base}_v{version}"
                            target_dir = os.path.join(split_parts_root, folder_name)
                            if not os.path.exists(target_dir):
                                break
                            version += 1
                        os.makedirs(target_dir, exist_ok=True)
                else:
                    os.makedirs(target_dir, exist_ok=True)
                
                # Try cache first!
                metadata, cached_obj_path = get_cached_model_details(model)
                raw_obj = cached_obj_path
                temp_dir = None
                
                if not metadata or not cached_obj_path:
                    # Cache miss - use lock
                    with _model_extract_lock:
                        # Re-check cache after acquiring lock
                        metadata, cached_obj_path = get_cached_model_details(model)
                        if not metadata or not cached_obj_path:
                            raw_obj, temp_dir = get_temp_raw_model(model, grp)
                            metadata = parse_obj_metadata(raw_obj)
                            save_model_to_cache(model, raw_obj, metadata)
                        else:
                            raw_obj = cached_obj_path
                
                # 2. Calculate scale factor
                # Original game coords are in meters, target is in mm
                original_wingspan = metadata["wingspan"]
                original_length = metadata["length"]
                
                if scale_mode == 'wingspan':
                    # target wingspan (mm) / original wingspan (m)
                    scale_factor = scale_value / original_wingspan
                elif scale_mode == 'length':
                    # target length (mm) / original length (m)
                    scale_factor = scale_value / original_length
                else: # multiplier
                    scale_factor = scale_value * 1000.0 # Convert meters to mm
                    
                # 3. Classify groups based on level
                category = vehicle_index.get(model, {}).get("category", "aircraft")
                groups_map = classify_groups(metadata["groups"], level, category)
                
                # Filter out excluded parts
                excluded_parts = params.get('excluded_parts', [])
                filtered_groups_map = {}
                for filename, target_groups in groups_map.items():
                    # Filter out any sub-group that is in the excluded list
                    active_groups = [g for g in target_groups if g not in excluded_parts and filename not in excluded_parts]
                    if active_groups:
                        filtered_groups_map[filename] = active_groups
                
                # Copy mtl file if it exists in base
                if temp_dir:
                    src_mtl = os.path.join(temp_dir, f"{model}.mtl")
                    if os.path.exists(src_mtl):
                        shutil.copy(src_mtl, os.path.join(OUTPUT_ROOT, f"{model}.mtl"))
                    
                # 5. Run segmenter
                files = run_segmentation_pipeline(raw_obj, target_dir, filtered_groups_map, scale_factor)
                
                # Cleanup
                if temp_dir and os.path.exists(temp_dir):
                    try:
                        shutil.rmtree(temp_dir)
                    except OSError:
                        pass
                
                response = {
                    "success": True,
                    "scale_factor": scale_factor,
                    "dimensions": {
                        "length": original_length * scale_factor,
                        "height": metadata["height"] * scale_factor,
                        "wingspan": original_wingspan * scale_factor
                    },
                    "files": files,
                    "groups_map": groups_map,
                    "folder_name": folder_name,
                    "output_dir": os.path.abspath(target_dir)
                }
                response_bytes = json.dumps(response).encode('utf-8')
                self.send_response_compressed(response_bytes, 'application/json')
            except Exception as e:
                self.send_response_compressed(json.dumps({"error": str(e)}).encode('utf-8'), 'application/json')

def watchdog_thread():
    global last_ping_time, ping_received
    import time
    # Wait for the first ping (maximum 15 seconds)
    start_wait = time.time()
    while not ping_received:
        if time.time() - start_wait > 15:
            print("Watchdog: Browser first ping timeout. Shutting down server...")
            os._exit(0)
        time.sleep(1)
        
    # Once first ping is received, check last_ping_time periodically
    while True:
        time.sleep(2)
        if time.time() - last_ping_time > 8: # 8 seconds threshold
            print("Watchdog: Browser tab closed. Shutting down server...")
            os._exit(0)

def main():
    # Start background watchdog thread
    watchdog = threading.Thread(target=watchdog_thread)
    watchdog.daemon = True
    watchdog.start()

    # Start background indexing thread
    indexing_thread = threading.Thread(target=scan_vehicles_thread)
    indexing_thread.daemon = True
    indexing_thread.start()
    
    # Run HTTP Server (threaded so thumbnail fetches don't block model loading)
    handler = WebManagerHandler
    class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True
        daemon_threads = True
    with ThreadedHTTPServer(("", PORT), handler) as httpd:
        print(f"Web Manager Server running at http://localhost:{PORT}")
        
        import webbrowser
        def open_browser():
            import time
            time.sleep(1)
            webbrowser.open(f'http://localhost:{PORT}')
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.server_close()

if __name__ == '__main__':
    main()
