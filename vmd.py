import os
import glob
import subprocess
import pandas as pd
import math

from utils import get_meta_data

def generate_vmd_script(xyz_file, output_dir):
    data_filename = os.path.basename(xyz_file).replace('.xyz', '.data')
    
    script_content = f"""#!/usr/bin/vmd
mol new "{xyz_file}" type xyz
cd "{output_dir}"
topo retypebonds
topo guessangles  
topo guessdihedrals
topo writelammpsdata "{data_filename}" full
quit
"""
    return script_content

def run_vmd_script(script_path):
    result = subprocess.run(['vmd', '-e', script_path], 
                            capture_output=True, 
                            text=True,
                            check=True)
    return True

def genereate_data_files(xyz_files_path, output_dir, script_name):
    os.makedirs(output_dir, exist_ok=True)

    xyz_files = glob.glob(xyz_files_path)
    
    if not xyz_files:
        print(f"No XYZ files found matching pattern: {xyz_files_path}")
        return
    
    print(f"Found {len(xyz_files)} XYZ files")
    print("=" * 50)
    
    success_count = 0
    
    for i, xyz_file in enumerate(xyz_files, 1):
        filename = os.path.basename(xyz_file)
        data_filename = filename.replace('.xyz', '.data')
        
        print(f"[{i}/{len(xyz_files)}] Processing: {filename}")
        
        script_content = generate_vmd_script(xyz_file, output_dir)
        script_path = os.path.join(output_dir, script_name)
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        
        print(f"  ✓ Generated: {script_name}")
        print(f"  Running VMD...")
        
        if run_vmd_script(script_path):
            print(f"  ✓ Successfully created: {data_filename}")
            success_count += 1
        else:
            print(f"  ✗ Failed to process: {filename}")
        
    print("\n" + "=" * 50)
    print("CONVERSION SUMMARY")
    print("=" * 50)
    print(f"Successfully processed: {success_count}/{len(xyz_files)} files")

    data_files = glob.glob(os.path.join(output_dir, "*.data"))
    if data_files:
        print(f"\nGenerated data files:")
        for data_file in data_files:
            file_size = os.path.getsize(data_file)
            print(f"  ✓ {os.path.basename(data_file)} ({file_size} bytes)")

def round_up_to_tenths(value):
    return math.ceil(value * 10) / 10

def calculate_box_dimensions(item):
    a = item.get('a', 1.0)
    b = item.get('b', 1.0)
    c = item.get('c', 1.0)

    super_cell = item.get('super_cell')
    
    xhi = round_up_to_tenths(float(a) * super_cell)
    yhi = round_up_to_tenths(float(b) * super_cell)
    zhi = round_up_to_tenths(float(c) * super_cell)
    
    return {
        'xlo_xhi': f"0.000000 {xhi:.6f}",
        'ylo_yhi': f"0.000000 {yhi:.6f}", 
        'zlo_zhi': f"0.000000 {zhi:.6f}"
    }

def edit_data_files(output_dir, meta_data):
    data_files = glob.glob(os.path.join(output_dir, "*.data"))
    
    if not data_files:
        print("No data files found to edit")
        return
    
    print("\n" + "=" * 50)
    print("EDITING DATA FILES")
    print("=" * 50)
    
    edited_count = 0
    
    for data_file in data_files:
        filename = os.path.basename(data_file)
        alloy_name = filename.replace('.data', '')
        
        matching_item = None
        for item in meta_data:
            if str(item.get('name', '')).strip() == alloy_name.strip():
                matching_item = item
                break
        
        if not matching_item:
            print(f"  ⚠ No meta data found for: {alloy_name}")
            continue
        
        print(f"Editing: {filename}")
        
        box_dims = calculate_box_dimensions(matching_item)
        
        try:
            with open(data_file, 'r') as f:
                lines = f.readlines()
            
            temp_file = data_file + '.tmp'
            
            with open(temp_file, 'w') as f:
                for line in lines:
                    if 'xlo xhi' in line:
                        f.write(f"{box_dims['xlo_xhi']}  xlo xhi\n")
                        print(f"    X: {box_dims['xlo_xhi']}")
                    elif 'ylo yhi' in line:
                        f.write(f"{box_dims['ylo_yhi']}  ylo yhi\n")
                        print(f"    Y: {box_dims['ylo_yhi']}")
                    elif 'zlo zhi' in line:
                        f.write(f"{box_dims['zlo_zhi']}  zlo zhi\n")
                        print(f"    Z: {box_dims['zlo_zhi']}")
                    else:
                        f.write(line)
            
            os.replace(temp_file, data_file)
            edited_count += 1
            print(f"  ✓ Successfully updated box dimensions")
            
        except Exception as e:
            print(f"  ✗ Error editing {filename}: {e}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    print("\n" + "=" * 50)
    print("EDITING SUMMARY")
    print("=" * 50)
    print(f"Successfully edited: {edited_count}/{len(data_files)} files")


def parse_meta_data_for_editing(meta_data_path):
    """Parse meta data specifically for editing data files"""
    meta_data = get_meta_data(meta_data_path)
    
    for item in meta_data:
        for param in ['a', 'b', 'c']:
            if param in item and item[param]:
                try:
                    item[param] = float(item[param])
                except (ValueError, TypeError):
                    item[param] = 1.0
            else:
                item[param] = 1.0
        
        if 'super_cell_parsed' not in item:
            super_cell = item.get('super_cell', '1')
            if isinstance(super_cell, (int, float)):
                item['super_cell_parsed'] = [int(super_cell)] * 3
            elif isinstance(super_cell, str):
                try:
                    if ',' in super_cell:
                        clean_str = super_cell.replace('[', '').replace(']', '').replace('(', '').replace(')', '')
                        cells = [int(x.strip()) for x in clean_str.split(',')]
                        if len(cells) == 1:
                            item['super_cell_parsed'] = cells * 3
                        else:
                            item['super_cell_parsed'] = cells[:3]
                    else:
                        cell_val = int(super_cell)
                        item['super_cell_parsed'] = [cell_val] * 3
                except (ValueError, AttributeError):
                    item['super_cell_parsed'] = [1, 1, 1]
            else:
                item['super_cell_parsed'] = [1, 1, 1]
    
    return meta_data


def xyz_to_data(xyz_files_path, output_dir, script_path, data):
    
    genereate_data_files(xyz_files_path, output_dir, script_path)    
    edit_data_files(output_dir, data)


if __name__ == "__main__":
    element = 'Ta_Co'

    xyz_files_path = f"./{element}/vesta/*.xyz"
    output_dir = f"./{element}/vmd"
    script_name = "script.tcl"
    meta_data_path = f'./{element}/data.xlsx'
    
    genereate_data_files(xyz_files_path, output_dir, script_name)
    
    print("\n" + "=" * 50)
    print("LOADING META DATA FOR EDITING")
    print("=" * 50)
    
    meta_data = parse_meta_data_for_editing(meta_data_path)
    
    print("Meta data loaded:")
    for idx, item in enumerate(meta_data):
        box_dims = calculate_box_dimensions(item)
        print(f"  {item.get('name')}: a={item.get('a')}, b={item.get('b')}, c={item.get('c')}, "
              f"super_cell={item.get('super_cell_parsed')} -> Box: {box_dims['xlo_xhi']} / {box_dims['ylo_yhi']} / {box_dims['zlo_zhi']}")
    
    edit_data_files(output_dir, meta_data)