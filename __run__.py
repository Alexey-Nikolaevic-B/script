import os
import time
import shutil
import pandas as pd
from pathlib import Path
import openpyxl
import numpy as np

import matplotlib.pyplot as plt
import pandas as pd

from src.supercell import make_supercell, cif_to_xyz
from src.vmd import xyz_to_data
from src.lammps import simulate


VESTA_PATH = Path('./_src/VESTA-gtk3/VESTA')
VMD_SCRIPT = Path('vmd_convert.tcl')
LAMMPS_TEMPLATE = Path('./src/template_formation.txt')

BASE_DIR = Path('calculations')
DATA_FILE = 'data.xlsx'
DATA_COLUMNS = ['name', 'major_element', 'minor_element', 'lattice_a', 'lattice_b', 'lattice_c', 'supercell_size', 'proto_major', 'proto_minor', 'prototype_name', 'cif_file', 'cif_link', 'space_group', 'run_simulation']
# FORMATION_COLUMNS = [name	Temp	Press	TotEng	v_Etot	c_E1	c_E2	v_formation_energy	v_heat_formation	v_lengtha	v_lengthc]

def add_new_alloy(element1, element2):
    alloy_folder = BASE_DIR / f"{element1}_{element2}"
    alloy_folder.mkdir(parents=True, exist_ok=True)

    cif_dir = alloy_folder / "cif"
    cif_dir.mkdir(exist_ok=True)
    
    excel_path = alloy_folder / 'data.xlsx'
    
    df = pd.DataFrame(columns=DATA_COLUMNS)
    df.to_excel(excel_path, index=False)


def clean_dirs(root_path):
    excluded_names = ['_cif']
    root_path = Path(root_path)
    
    if not root_path.exists():
        print(f"Path '{root_path}' does not exist")
        return
    
    for item in root_path.iterdir():
        if item.is_dir() and item.name not in excluded_names:
            try:
                shutil.rmtree(item)
                print(f"Deleted: {item}")
            except Exception as e:
                print(f"Error deleting {item}: {e}")


def run_simulation(selected_dir):
    working_dir = BASE_DIR / selected_dir

    data_path = working_dir / DATA_FILE
    alloys = pd.read_excel(data_path)
    alloys['run_simulation'] = alloys['run_simulation'].astype(str).str.lower().map({
        'true': True, 'false': False
    })

    cross_potential_file = f"{selected_dir}.meam"
    meam_file = working_dir/ cross_potential_file
    library_file = working_dir / "library.meam"

    simulation_name = input('\nCurrent simulation: ').strip()
    simulation_dir = working_dir / simulation_name

    simulation_dir.mkdir(exist_ok=True)
    clean_dirs(simulation_dir)

    for index, alloy in alloys.iterrows():
        if not alloy["run_simulation"]:
            continue

        alloy_name = alloy['name']
        alloy_dir = simulation_dir / alloy_name
        alloy_dir.mkdir(exist_ok=True)

        proto_cif = BASE_DIR / selected_dir / "_cif" / alloy['cif_file']
        new_cif = alloy_dir / f"{alloy_name}.cif"
        lattice_params = (alloy['lattice_a'], alloy['lattice_b'], alloy['lattice_c'])

        element_mapping = {alloy['proto_major']:alloy['major_element'], alloy['proto_minor']:alloy['minor_element']}
        supercell_matrix = (alloy['supercell_size'], alloy['supercell_size'], alloy['supercell_size'])
        structure = make_supercell(proto_cif, lattice_params, supercell_matrix, new_cif, element_mapping)

        output_file = alloy_dir / f"{alloy_name}.xyz"

        cif_to_xyz(structure, output_file)
        xyz_to_data(output_file, alloy_dir, VMD_SCRIPT, alloy['lattice_a'], alloy['lattice_b'], alloy['lattice_c'], 4)


    columns = ['Name', 'Step', 'Temp', 'Press', 'TotEng', 'v_Etot', 'c_E1', 'c_E2', 'v_formation_energy', 'v_heat_formation', 'v_lengtha', 'v_lengthc']
    df = pd.DataFrame(columns=columns)
    formation_excel_path = simulation_dir / 'formation.xlsx'
    df.to_excel(formation_excel_path, index=False)

    formation_combined = []

    for index, alloy in alloys.iterrows():
        if not alloy["run_simulation"]:
            continue
        formation_calculated = False
        alloy_name = alloy['name']
        alloy_dir = simulation_dir / alloy_name
        element1 = 'Co'
        element2 = 'Ta'

        alloy_data = f"{alloy_name}.data"
        
        shutil.copy2(library_file, alloy_dir / "library.meam")
        shutil.copy2(meam_file, alloy_dir / f"{selected_dir}.meam")

        lammps_code = 'formation.lmp'
        if not simulate(LAMMPS_TEMPLATE, element1, element2, alloy_dir, alloy_data, f"{selected_dir}.meam", "library.meam", lammps_code, alloy['supercell_size'], alloy['Co_index'], alloy['Ta_index'], alloy['coef']):
            continue

        log_file = alloy_dir / 'log.lammps'
        with open(log_file) as f:
            for line in f:
                if line.strip().startswith('10000'):
                    formation_calculated = line.strip().split()
                    break

        formation = pd.read_excel(formation_excel_path)
        if formation_calculated:  # Check if list has items
            formation_calculated = [alloy_name] + formation_calculated
            formation_combined.append([alloy_name, float(formation_calculated[8])])
        
        formation.loc[len(formation)] = formation_calculated
        formation.to_excel(formation_excel_path, index=False)

    formation_excel_path = working_dir / 'formation.xlsx'
    df = pd.read_excel(formation_excel_path)
    df[simulation_name] = np.nan

    for alloy_name, new_value in formation_combined:
        mask = df['name'] == alloy_name
        if mask.any():
            df.loc[mask, simulation_name] = new_value
        else:
            print(f"Warning: Alloy '{alloy_name}' from formation_combined not found in the table")

    df.to_excel(formation_excel_path, index=False)
      
            
if __name__ == '__main__':
    BASE_DIR.mkdir(exist_ok=True)
    
    while True:
        print("\n[1] Add alloy\n[2] Run simulation\n[3] Exit")
        choice = input("Choose: ").strip()
        
        if choice == '1':
            elem1 = input('First element: ').strip()
            elem2 = input('Second element: ').strip()
            add_new_alloy(elem1, elem2)
        elif choice == '2':
            dirs = [d for d in BASE_DIR.iterdir() if d.is_dir()]
            for i, d in enumerate(dirs, 1):
                print(f"[{i}] {d.name}")
            
            if dirs:
                try:
                    selected = int(input("Select: ").strip()) - 1
                    if 0 <= selected < len(dirs):
                        print(f"Running: {dirs[selected].name}")
                        run_simulation(dirs[selected].name)
                except ValueError:
                    print("Invalid selection1")
        elif choice == '3':
            break