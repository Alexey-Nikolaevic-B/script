import os
import time
import shutil

import vesta
import vmd

from lammps import simulate
from utils import get_meta_data

VESTA_PATH = './VESTA-gtk3/VESTA'
VMD_SCRIPT = './vmd_convert.tcl'
LAMMPS_TEMPLATE = './template_formation.txt'

BASE_DIR = '.'
DATA_FILE = 'data.xlsx'
DATA_COLUMNS = ['name', 'major_element', 'minor_element', 'lattice_a', 'lattice_b', 'lattice_c', 'supercell_size', 'proto_major', 'proto_minor', 'cif_file']

def create_alloy(element1, element2):
    pass

def clean_dirs(selected_dir):
    pass

def run_simulation(selected_dir):
    clean_dirs(selected_dir)

    data_path = f'{selected_dir}/{DATA_FILE}'
    alloys = get_meta_data(data_path)
    
    meam_file = f'{selected_dir}/CoTa.meam'
    library_file = f'{selected_dir}/library.meam'

    # for alloy_data in alloys:
    #     if not alloy_data.get('run_simulation'):
    #         continue

    #     lattice_a = float(alloy_data.get('lattice_a'))
    #     lattice_b = float(alloy_data.get('lattice_b'))
    #     lattice_c = float(alloy_data.get('lattice_c'))
    #     supercell_size= float(alloy_data.get('supercell_size'))
        
    #     alloy_name = alloy_data['name']
    #     alloy_dir = f'{selected_dir}/{alloy_name}'

    #     os.makedirs(alloy_dir, exist_ok=True)

    #     shutil.copy2(meam_file, alloy_dir)
    #     shutil.copy2(library_file, alloy_dir)

    #     prototype = alloy_data['cif_file']
    #     cif_file = f'{selected_dir}/cif/{prototype}'
    #     output_path = f'./{alloy_name}/{alloy_name}'

    #     vesta.launch_vesta(VESTA_PATH, cif_file)
    #     time.sleep(2)

    #     vesta.open_edit_data()
    #     vesta.set_alloy_name(alloy_data['name'])
    #     vesta.adjust_lattice(alloy_data.get('lattice_a'), alloy_data.get('lattice_b'), alloy_data.get('lattice_c'))
    #     vesta.create_supercell(alloy_data.get('supercell_size'))
    #     vesta.export_file(output_path)

    #     major_new, major_old = alloy_data['major_element']
    #     minor_new, minor_old = alloy_data['minor_element']
    #     vesta.update_elements(output_path, major_new, major_old, minor_new, minor_old)

    # for alloy_data in alloys:
    #     if not alloy_data.get('run_simulation'):
    #         continue

    #     lattice_a = float(alloy_data.get('lattice_a'))
    #     lattice_b = float(alloy_data.get('lattice_b'))
    #     lattice_c = float(alloy_data.get('lattice_c'))
    #     supercell_size= float(alloy_data.get('supercell_size'))
        
    #     alloy_name = alloy_data['name']
    #     alloy_dir = f'{selected_dir}/{alloy_name}'
            
    #     xyz_file = f'{alloy_dir}/{alloy_name}.xyz'
    #     vmd.convert_xyz_to_data(xyz_file, alloy_dir, VMD_SCRIPT, lattice_a, lattice_b, lattice_c, supercell_size)

    for alloy_data in alloys:
        if not alloy_data.get('run_simulation'):
            continue
        
        alloy_name = alloy_data['name']
        alloy_dir = f'{selected_dir}/{alloy_name}'
        major_new, major_old = alloy_data['major_element']
        minor_new, minor_old = alloy_data['minor_element']

        alloy_data = f'{alloy_name}.data'
        cross_potential_file = 'CoTa.meam'

        simulate(LAMMPS_TEMPLATE, major_new, minor_new, alloy_dir, alloy_data, cross_potential_file)
        

if __name__ == '__main__':
    while True:
        print("\n1. Add alloy\n2. Run simulation\n3. Exit")
        choice = int(input("Choose: "))
        
        if choice == 1:
            elem1 = input('First element: ')
            elem2 = input('Second element: ')
            create_alloy(elem1, elem2)
        elif choice == 2:
            dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
            for i, d in enumerate(dirs, 1):
                print(f"{i}. {d}")
            
            if dirs:
                selected = int(input("Select: ")) - 1
                if 0 <= selected < len(dirs):
                    print(f"Running: {dirs[selected]}")
                    run_simulation(dirs[selected])
        elif choice == 3:
            break