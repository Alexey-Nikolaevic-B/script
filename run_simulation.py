import os
import pandas as pd

from vesta import cif_to_xyz
from vmd import xyz_to_data
from lammps import simulate

from utils import get_meta_data

VESTA_LAUNCHER_PATH = './VESTA-gtk3/VESTA'
VMD_SCRIPT_PATH = './vmd_convert.tcl'
LAMMPS_TEMLPATE = './template_formation.txt'

BASE_PATH = '.'
VESTA_FOLDER = 'vesta'
VMD_FOLDER = 'vmd' 
LAMMPS_FOLDER = 'lammps'
CIF_FOLDER = 'cif'

DATA_HEADERS = ['name', 'major', 'minor', 'a', 'b', 'c', 'super_cell', 'prototype major', 'prototype minor', 'prototype']
DATA_FILE_NAME = 'data'

def add_new_alloy(element1, element2):
    alloy_folder = f'{BASE_PATH}/{element1}_{element2}'
    
    os.makedirs(alloy_folder, exist_ok=True)
    
    folders = [
        os.path.join(alloy_folder, VESTA_FOLDER),
        os.path.join(alloy_folder, VMD_FOLDER),
        os.path.join(alloy_folder, LAMMPS_FOLDER), 
        os.path.join(alloy_folder, CIF_FOLDER)
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created: {folder}")
    
    excel_path = os.path.join(alloy_folder, f'{DATA_FILE_NAME}.xlsx')
    
    df = pd.DataFrame(columns=DATA_HEADERS)
    df.to_excel(excel_path, index=False)
    print(f"Created Excel file: {excel_path}")


def clear_folders(alloy_folder):
    folders_to_clear = [VESTA_FOLDER, VMD_FOLDER, LAMMPS_FOLDER]
    
    for folder_name in folders_to_clear:
        folder_path = os.path.join(alloy_folder, folder_name)
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        import shutil
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Error clearing {file_path}: {e}")
            print(f"Cleared: {folder_path}")
        else:
            print(f"Folder doesn't exist: {folder_path}")

def run_sim(selected_folder):
    clear_folders(selected_folder)

    data_path = f'{selected_folder}/{DATA_FILE_NAME}.xlsx'
    data = get_meta_data(data_path)
    print("=== PARSED DATA ===")
    for idx, item in enumerate(data):
        print(f"Alloy № {idx}:")
        print(f"  Alloy: {item.get('name')}")
        print(f"  Elements: {item.get('elements')}")
        print(f"  Parsed Elements: {item.get('elements_parsed')}")
        print(f"  Major Element: {item.get('major_element')}")
        print(f"  Minor Element: {item.get('minor_element')}")
        print(f"  a: {item.get('a')}")
        print(f"  b: {item.get('b')}")
        print(f"  c: {item.get('c')}")
        print(f"  Prototype: {item.get('prototype')}")
        print()

    cif_path = f'./{selected_folder}/{CIF_FOLDER}'
    cif_to_xyz(VESTA_LAUNCHER_PATH, cif_path, data)

    xyz_path = f'./{selected_folder}/{VESTA_FOLDER}'
    data_path = f'./{selected_folder}/{LAMMPS_FOLDER}'
    xyz_to_data(xyz_path, data_path, VMD_SCRIPT_PATH, data)
    
    lammps_path = f'./{selected_folder}/{LAMMPS_FOLDER}'
    simulate(LAMMPS_TEMLPATE, item.get('major_element')[0], item.get('minor_element')[0], lammps_path)
   
if __name__ == '__main__':
    element1 = ''
    element2 = ''

    while True:
        print("\n[1] Add new alloy")
        print("[2] Run simulation for alloy") 
        print("[3] Exit")
        
        choice = int(input("Select option: "))
        
        if choice == 1:
            element1 = input('First elemet: ')
            element2 = input('Second elemet: ')

            add_new_alloy(element1, element2)
        elif choice == 2:
            print("Available folders:")
            folders = [f for f in os.listdir('.') if os.path.isdir(f)]
            for i, folder in enumerate(folders, 1):
                print(f"[{i}] {folder}")   
            if folders:
                choice = int(input("Select folder (number): "))
                if 1 <= choice <= len(folders):
                    selected_folder = folders[choice-1]
                    
                    print(f"Running simulation for: {selected_folder}")
                    run_sim(selected_folder)
                else:
                    print("Invalid selection")
            else:
                print("No folders found")

        elif choice == 3:
            break
        else:
            print("Invalid option")