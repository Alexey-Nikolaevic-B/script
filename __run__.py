import os
import time
import shutil
import pandas as pd


from src.supercell import make_supercell, cif_to_xyz
from src.vmd import xyz_to_data
from src.lammps import simulate


VESTA_PATH = './_src/VESTA-gtk3/VESTA'
VMD_SCRIPT = 'vmd_convert.tcl'
LAMMPS_TEMPLATE = './src/template_formation.txt'

BASE_DIR = 'calculations'
DATA_FILE = 'data.xlsx'
DATA_COLUMNS = ['name', 'major_element', 'minor_element', 'lattice_a', 'lattice_b', 'lattice_c', 'supercell_size', 'proto_major', 'proto_minor', 'prototype_name', 'cif_file', 'cif_link', 'space_group', 'run_simulation']

def get_meta_data(path):
    df = pd.read_excel(path)
    parsed_data = []
    
    for idx, row in df.iterrows():
        row_dict = row.to_dict()
        
        if 'run_simulation' in row_dict:
            run_sim = row_dict['run_simulation']
            
            if isinstance(run_sim, bool):
                row_dict['run_simulation'] = run_sim
            elif isinstance(run_sim, str):
                cleaned = run_sim.strip().strip('"\'')
                if cleaned.lower() in ['true', 'yes', '1', 'да']:
                    row_dict['run_simulation'] = True
                elif cleaned.lower() in ['false', 'no', '0', 'нет']:
                    row_dict['run_simulation'] = False
                else:
                    row_dict['run_simulation'] = False
            elif isinstance(run_sim, (int, float)):
                row_dict['run_simulation'] = bool(run_sim)
            else:
                row_dict['run_simulation'] = False
        
        original_major = row_dict.get('major_element', '')
        original_minor = row_dict.get('minor_element', '')
        prototype_major = row_dict.get('proto_major', '')
        prototype_minor = row_dict.get('proto_minor', '')
        
        if original_major and original_minor:
            major_clean = ''.join([char for char in str(original_major) if not char.isdigit()])
            minor_clean = ''.join([char for char in str(original_minor) if not char.isdigit()])
            row_dict['elements_parsed'] = f"{major_clean} {minor_clean}"
        else:
            row_dict['elements_parsed'] = ""
        
        major_clean = ''.join([char for char in str(original_major) if not char.isdigit()]) if original_major else None
        minor_clean = ''.join([char for char in str(original_minor) if not char.isdigit()]) if original_minor else None
        proto_major_clean = ''.join([char for char in str(prototype_major) if not char.isdigit()]) if prototype_major else ''
        proto_minor_clean = ''.join([char for char in str(prototype_minor) if not char.isdigit()]) if prototype_minor else ''
        
        row_dict['major_element'] = [major_clean, proto_major_clean]
        row_dict['minor_element'] = [minor_clean, proto_minor_clean]
        
        for param in ['lattice_a', 'lattice_b', 'lattice_c']:
            if param in row_dict:
                if pd.notna(row_dict[param]) and row_dict[param] not in ['', 'None', None]:
                    row_dict[param] = float(row_dict[param])
                else:
                    row_dict[param] = ""
        
        if 'cif_file' in row_dict and pd.notna(row_dict['cif_file']):
            cif_str = str(row_dict['cif_file'])
            if not cif_str.endswith('.cif'):
                row_dict['cif_file'] = cif_str + '.cif'
        
        parsed_data.append(row_dict)
    
    return parsed_data

def add_new_alloy(element1, element2):
    alloy_folder = f'{BASE_DIR}/{element1}_{element2}'
    
    os.makedirs(alloy_folder, exist_ok=True)

    cif_dir = f'{BASE_DIR}/{element1}_{element2}/cif'
    os.makedirs(cif_dir, exist_ok=True)
    
    excel_path = os.path.join(alloy_folder, 'data.xlsx')
    
    df = pd.DataFrame(columns=DATA_COLUMNS)
    df.to_excel(excel_path, index=False)

def clean_dirs(root_path):
    excluded_names = '_cif'
    if not os.path.exists(root_path):
        print(f"Path '{root_path}' does not exist")
        return
    
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        
        if os.path.isdir(item_path) and item not in excluded_names:
            try:
                shutil.rmtree(item_path)
                print(f"Deleted: {item_path}")
            except Exception as e:
                print(f"Error deleting {item_path}: {e}")

def run_simulation(selected_dir):
    clean_path = f'{BASE_DIR}/{selected_dir}'
    clean_dirs(clean_path)

    data_path = f'{BASE_DIR}/{selected_dir}/{DATA_FILE}'
    alloys = get_meta_data(data_path)   

    cross_potential_file = f'{selected_dir}.meam'
    meam_file = f'{BASE_DIR}/{selected_dir}/{cross_potential_file}'
    library_file = f'{BASE_DIR}/{selected_dir}/library.meam'

    for alloy in alloys:
        if not alloy.get('run_simulation'):
            continue
        
        element = alloy['name']
        new_dir = f'{BASE_DIR}/{selected_dir}/{element}'
        os.makedirs(new_dir, exist_ok=True)

        proto_cif = f'{BASE_DIR}/{selected_dir}/_cif/{alloy['cif_file']}'
        new_cif = f'{BASE_DIR}/{selected_dir}/{element}/{element}.cif'
        lattice_params = (alloy['lattice_a'], alloy['lattice_b'], alloy['lattice_c'])

        element_mapping = {alloy['major_element'][1]:alloy['major_element'][0], alloy['minor_element'][1]:alloy['minor_element'][0]}

        structure = make_supercell(proto_cif, lattice_params, (4,4,4), new_cif, element_mapping)

        output_file = f'{BASE_DIR}/{selected_dir}/{element}/{element}.xyz'
        cif_to_xyz(structure, output_file)
        xyz_to_data(output_file, new_dir, VMD_SCRIPT, alloy['lattice_a'], alloy['lattice_b'], alloy['lattice_c'], 4)

    for alloy in alloys:
        if not alloy.get('run_simulation'):
            continue
        
        alloy_name = alloy['name']
        alloy_dir = f'{BASE_DIR}/{selected_dir}/{alloy_name}'
        major_new, major_old = alloy['major_element']
        minor_new, minor_old = alloy['minor_element']

        alloy_data = f'{alloy_name}.data'
        
        element = alloy['name']
        new_dir = f'{BASE_DIR}/{selected_dir}/{element}'
        shutil.copy2(library_file, os.path.join(new_dir, "library.meam"))
        shutil.copy2(meam_file, os.path.join(new_dir, "Ta_Co.meam"))

        lammps_code = 'formation.lmp'
        simulate(LAMMPS_TEMPLATE, major_new, minor_new, alloy_dir, alloy_data, "Ta_Co.meam", "library.meam", lammps_code)
        
if __name__ == '__main__':
    while True:
        print("\n[1] Add alloy\n[2] Run simulation\n[3] Exit")
        choice = int(input("Choose: "))
        
        if choice == 1:
            elem1 = input('First element: ')
            elem2 = input('Second element: ')
            add_new_alloy(elem1, elem2)
        elif choice == 2:
            dirs = [d for d in os.listdir(BASE_DIR) 
                    if os.path.isdir(os.path.join(BASE_DIR, d))]
            for i, d in enumerate(dirs, 1):
                print()
                print(f"[{i}] {d}")
            
            if dirs:
                selected = int(input("Select: ")) - 1
                if 0 <= selected < len(dirs):
                    print(f"Running: {dirs[selected]}")
                    run_simulation(dirs[selected])
        elif choice == 3:
            break