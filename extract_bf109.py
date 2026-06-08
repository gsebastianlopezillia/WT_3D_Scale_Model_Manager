import os
import sys
import shutil
import json

# Add dagor_explorer/src/dae to python path
sys.path.append(os.path.abspath(r'.\dagor_explorer\src\dae'))

from parse.gameres import GameResourcePack, GameResDesc
from parse.material import DDSxTexturePack2
from util.assetcacher import AssetCacher

def clean_and_split_obj(raw_obj_path, clean_obj_path, output_dir, groups_map, target_wingspan_mm=None):
    exclude_groups = {
        'flare1', 'flare2', 'flare3', 'flare4', 'flare5', 'flare6', 'flare7', 'flare8', 'flare9', 'flare10',
        'fire1_1', 'fire1_2', 'fire1_3', 'fire1_4', 'fire1_5', 'fire1_6', 'fire1_7', 'fire1_8', 'fire1_9', 'fire1_10', 'fire1_11', 'fire1_12',
        'prop02_1', 'prop03_1', 'prop_side_1', 'prop01_1_dmg', 'Object001'
    }
    
    print("Parsing raw OBJ file...")
    vertices = []
    uvs = []
    normals = []
    
    group_faces = {}
    current_group = None
    current_material = None
    
    with open(raw_obj_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()
                vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
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
                    
    # 1. Write the full cleaned model (excluding flares, fire, animated propellers)
    cleaned_group_faces = {g: faces for g, faces in group_faces.items() if g not in exclude_groups}
    
    # Calculate bounds of the cleaned model to determine original wingspan
    cleaned_v_indices = set()
    for g, faces in cleaned_group_faces.items():
        for face_verts, mat in faces:
            for v_idx, vt_idx, vn_idx in face_verts:
                cleaned_v_indices.add(v_idx)
                
    if cleaned_v_indices:
        all_zs_orig = [vertices[idx][2] for idx in cleaned_v_indices]
        wingspan_m = max(all_zs_orig) - min(all_zs_orig)
        
        if target_wingspan_mm is not None:
            scale_factor = target_wingspan_mm / wingspan_m
            print(f"Original wingspan: {wingspan_m:.3f} meters")
            print(f"Applying scale factor: {scale_factor:.6f} to reach target wingspan of {target_wingspan_mm:.1f} mm")
            vertices = [(v[0] * scale_factor, v[1] * scale_factor, v[2] * scale_factor) for v in vertices]
        else:
            print(f"Original wingspan: {wingspan_m:.3f} meters (No scaling applied)")
    
    v_map = {}
    vt_map = {}
    vn_map = {}
    new_vertices = []
    new_uvs = []
    new_normals = []
    
    for g, faces in cleaned_group_faces.items():
        for face_verts, mat in faces:
            for v_idx, vt_idx, vn_idx in face_verts:
                if v_idx not in v_map:
                    v_map[v_idx] = len(new_vertices)
                    new_vertices.append(vertices[v_idx])
                if vt_idx != -1 and vt_idx not in vt_map:
                    vt_map[vt_idx] = len(new_uvs)
                    new_uvs.append(uvs[vt_idx])
                if vn_idx != -1 and vn_idx not in vn_map:
                    vn_map[vn_idx] = len(new_normals)
                    new_normals.append(normals[vn_idx])
                    
    print(f"Full Cleaned Model: Vertices={len(new_vertices)}, Faces={sum(len(x) for x in cleaned_group_faces.values())}")
    
    with open(clean_obj_path, 'w') as f:
        f.write("mtllib bf_109g_6.mtl\n")
        for v in new_vertices:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
        for vt in new_uvs:
            f.write(f"vt {vt[0]:.4f} {vt[1]:.4f}\n")
        for vn in new_normals:
            f.write(f"vn {vn[0]:.4f} {vn[1]:.4f} {vn[2]:.4f}\n")
            
        for g, faces in cleaned_group_faces.items():
            f.write(f"g {g}\n")
            last_mat = None
            for face_verts, mat in faces:
                if mat != last_mat:
                    f.write(f"usemtl {mat}\n")
                    last_mat = mat
                
                f_parts = []
                for v_idx, vt_idx, vn_idx in face_verts:
                    new_v = v_map[v_idx] + 1
                    new_vt = vt_map[vt_idx] + 1 if vt_idx != -1 else ""
                    new_vn = vn_map[vn_idx] + 1 if vn_idx != -1 else ""
                    f_parts.append(f"{new_v}/{new_vt}/{new_vn}")
                f.write(f"f {' '.join(f_parts)}\n")
                
    # Print clean bounds for reference
    all_xs = [v[0] for v in new_vertices]
    all_ys = [v[1] for v in new_vertices]
    all_zs = [v[2] for v in new_vertices]
    unit_str = "mm" if target_wingspan_mm is not None else "meters"
    print("\nCleaned Model Bounds:")
    print(f"  Length (X): {max(all_xs)-min(all_xs):.3f} {unit_str}")
    print(f"  Height (Y): {max(all_ys)-min(all_ys):.3f} {unit_str}")
    print(f"  Wingspan (Z): {max(all_zs)-min(all_zs):.3f} {unit_str}")
    
    # 2. Write split files
    split_dir = os.path.join(output_dir, 'split_parts')
    if os.path.exists(split_dir):
        shutil.rmtree(split_dir)
    os.makedirs(split_dir, exist_ok=True)
    
    print("\nWriting split components to 'split_parts' directory...")
    for filename, target_groups in groups_map.items():
        file_group_faces = {g: group_faces[g] for g in target_groups if g in group_faces}
        total_faces = sum(len(faces) for faces in file_group_faces.values())
        if total_faces == 0:
            continue
            
        # Re-index for this specific file
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
                        
        sub_out_path = os.path.join(split_dir, f"{filename}.obj")
        print(f"  Saved {filename}.obj (Verts: {len(sub_vertices)}, Faces: {total_faces})")
        
        with open(sub_out_path, 'w') as f:
            f.write("mtllib ../bf_109g_6.mtl\n") # point to the parent material file
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

def main():
    print("=== Bf 109 G-6 Extraction Pipeline ===")
    
    # Load path settings from config.json if it exists, otherwise use defaults
    config = {
        "wt_root": r'C:\Program Files (x86)\Steam\steamapps\common\War Thunder',
        "output_root": r'.\Bf109_Raw_Asset'
    }
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                if "wt_root" in user_config: config["wt_root"] = user_config["wt_root"]
                elif "WT_ROOT" in user_config: config["wt_root"] = user_config["WT_ROOT"]
                if "output_root" in user_config: config["output_root"] = user_config["output_root"]
                elif "OUTPUT_ROOT" in user_config: config["output_root"] = user_config["OUTPUT_ROOT"]
        except Exception as e:
            print(f"Error loading config.json: {e}")

    wt_root = config["wt_root"]
    output_dir = os.path.abspath(config["output_root"])
    
    # Clean output dir
    if os.path.exists(output_dir):
        print(f"Cleaning existing directory: {output_dir}")
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Load dynModelDesc.bin
    desc_path = os.path.join(wt_root, r'content\base\res\dynModelDesc.bin')
    print(f"Loading descriptors from {desc_path}...")
    if not os.path.exists(desc_path):
        print(f"ERROR: Descriptor file not found at {desc_path}")
        sys.exit(1)
        
    desc = GameResDesc(desc_path)
    desc.loadDataBlock()
    AssetCacher.appendGameResDesc(desc)
    
    # 2. Load and cache texture packages
    dxp_paths = [
        r'content.hq\hq_tex\res\hq_tex_aircrafts\bf_109.dxp.bin',
        r'content.hq\hq_tex\res\hq_tex_aircrafts\aircrafts.dxp.bin',
        r'content\base\res\aircrafts\aircrafts.dxp.bin',
        r'content\base\res\aircrafts\bf_109-hq.dxp.bin',
        r'content.hq\hq_tex\res\hq_tex_aircrafts\bf_109f_4.dxp.bin',
        r'content\base\res\aircrafts\germ_aircrafts.dxp.bin',
        r'content.hq\hq_tex\res\hq_tex_aircrafts\germ_aircrafts.dxp.bin',
        r'content\base\res\aircrafts\aircrafts-hq.dxp.bin',
        r'content.hq\hq_tex\res\hq_tex_aircrafts.dxp.bin'
    ]
    
    print("Caching texture archives...")
    for rel_path in dxp_paths:
        full_path = os.path.join(wt_root, rel_path)
        if os.path.exists(full_path):
            print(f"  Caching {os.path.basename(full_path)}...")
            try:
                dxp = DDSxTexturePack2(full_path)
                for ddsx in dxp.getPackedFiles():
                    if ddsx:
                        AssetCacher.cacheAsset(ddsx)
            except Exception as e:
                print(f"  WARNING: Failed to parse {full_path}: {e}")
        else:
            print(f"  Skipping (not found): {rel_path}")
            
    # 3. Load aircraft GRP, skeleton, and model
    grp_path = os.path.join(wt_root, r'content\base\res\aircrafts\germ_bf_109.grp')
    print(f"Loading models GRP from {grp_path}...")
    if not os.path.exists(grp_path):
        print(f"ERROR: GRP file not found at {grp_path}")
        sys.exit(1)
        
    grp = GameResourcePack(grp_path)
    
    # Cache skeleton first (bf_109g_6_skeleton is at index 82)
    print("Loading and caching skeleton resource...")
    skeleton_res = grp.getRealResource(82)
    AssetCacher.cacheAsset(skeleton_res)
    
    # bf_109g_6 is at resource index 83
    dyn_model = grp.getRealResource(83)
    dyn_model.computeData()
    
    # 4. Get LOD 0 model and export raw files temporarily
    mdl = dyn_model.getModel(0)
    mdl._Model__exportName = "bf_109g_6" # bypass read-only property to name files correctly
    
    print(f"Exporting raw files temporarily to: {output_dir}")
    mdl.exportObj(output_dir, exportTexture=True)
    
    # 5. Clean up OBJ by removing glitched/non-manifold game parts and splitting
    raw_obj_path = os.path.join(output_dir, 'bf_109g_6.obj')
    temp_raw_path = os.path.join(output_dir, 'bf_109g_6_raw.obj')
    os.rename(raw_obj_path, temp_raw_path)
    
    groups_map = {
        # Fuselage & Wings (Detailed decomposition)
        'bf_109g_6_fuselage': ['fuse'],
        'bf_109g_6_tail_section': ['tail'],
        'bf_109g_6_wing_left': ['wing_l'],
        'bf_109g_6_wing_right': ['wing_r'],
        'bf_109g_6_radiator_left': ['radiator1'],
        'bf_109g_6_radiator_right': ['radiator2'],
        'bf_109g_6_radiator_oil': ['radiator_oil1'],
        'bf_109g_6_antenna': ['antenna'],
        
        # Propeller & Canopy
        'bf_109g_6_propeller': ['prop01_1'],
        'bf_109g_6_canopy': ['blister1'],
        
        # Control Surfaces (Detailed decomposition)
        'bf_109g_6_rudder': ['rudder'],
        'bf_109g_6_elevator_left': ['elevator0'],
        'bf_109g_6_elevator_right': ['elevator1'],
        'bf_109g_6_aileron_left': ['aileron_l'],
        'bf_109g_6_aileron_right': ['aileron_r'],
        'bf_109g_6_flaps_left': ['flap_l', 'flap1_l', 'flap2_l'],
        'bf_109g_6_flaps_right': ['flap_r', 'flap1_r', 'flap2_r'],
        'bf_109g_6_slat_left': ['slat_l'],
        'bf_109g_6_slat_right': ['slat_r'],
        
        # Landing Gear (Separated struts from wheels)
        'bf_109g_6_gear_strut_left': ['gear_l'],
        'bf_109g_6_gear_wheel_left': ['wheel_l'],
        'bf_109g_6_gear_strut_right': ['gear_r'],
        'bf_109g_6_gear_wheel_right': ['wheel_r'],
        'bf_109g_6_gear_strut_tail': ['gear_c'],
        'bf_109g_6_gear_wheel_tail': ['wheel_c'],
        
        # Armament (Detailed decomposition)
        'bf_109g_6_bomb_rack_1': ['pylon_bomb1'],
        'bf_109g_6_bomb_rack_2': ['pylon_bomb2'],
        'bf_109g_6_cannon_pod_l': ['pylon_cannon_l'],
        'bf_109g_6_cannon_pod_r': ['pylon_cannon_r'],
        'bf_109g_6_cannon_pod_empty_l': ['pylon_cannon_empty_l'],
        'bf_109g_6_cannon_pod_empty_r': ['pylon_cannon_empty_r'],
        'bf_109g_6_cannon_pod_r6_l': ['pylon_cannon_r6_l'],
        'bf_109g_6_cannon_pod_r6_r': ['pylon_cannon_r6_r'],
        'bf_109g_6_rocket_tube_left': ['210mm_tube_l'],
        'bf_109g_6_rocket_tube_right': ['210mm_tube_r']
    }
    
    target_wingspan_mm = 900.0  # Target wingspan for 3D printing in mm
    clean_and_split_obj(temp_raw_path, raw_obj_path, output_dir, groups_map, target_wingspan_mm=target_wingspan_mm)
    os.remove(temp_raw_path)
    
    print("Export, clean-up, and splitting completed successfully!")

if __name__ == "__main__":
    main()
