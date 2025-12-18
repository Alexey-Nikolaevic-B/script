#!/usr/bin/env python

import sys
import re
import os
from pathlib import Path

from ase.io import read
from pymatgen.io.cif import CifParser, CifWriter
from pymatgen.io.lammps.data import LammpsData
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.core.structure import Structure
from pymatgen.core.lattice import Lattice
from pymatgen.io.xyz import XYZ

def make_supercell(cif_input, lattice_params, supercell_matrix, cif_output, element_mapping):
    # Convert cif_output to Path if it isn't already
    if not isinstance(cif_output, Path):
        cif_output = Path(cif_output)
    
    # Convert cif_input to string for pymatgen
    cif_input_str = str(cif_input) if isinstance(cif_input, Path) else cif_input
    
    structure = Structure.from_file(cif_input_str)
    
    if element_mapping:
        for site in structure:
            if site.species_string in element_mapping:
                site.species = element_mapping[site.species_string]
    
    new_lattice = Lattice.from_parameters(
        a=lattice_params[0],
        b=lattice_params[1],  
        c=lattice_params[2],
        alpha=90.0,
        beta=90.0,
        gamma=90.0
    )
    structure.lattice = new_lattice
    print(supercell_matrix)
    structure.make_supercell(supercell_matrix, to_unit_cell=True)
    
    # FIX: Use Path methods instead of string concatenation
    temp_cif = cif_output.with_name(cif_output.name + ".temp")
    
    writer = CifWriter(structure)
    writer.write_file(str(temp_cif))  # Convert to string for write_file
    
    if element_mapping:
        with open(temp_cif, 'r') as f:
            cif_content = f.read()
        
        for old_elem, new_elem in element_mapping.items():
            pattern1 = re.compile(r'\b' + re.escape(old_elem) + r'\s')
            pattern2 = re.compile(r'\b' + re.escape(old_elem) + r'(\d+)')
            cif_content = pattern1.sub(new_elem + ' ', cif_content)
            cif_content = pattern2.sub(new_elem + r'\1', cif_content)
        
        with open(cif_output, 'w') as f:
            f.write(cif_content)
        
        os.remove(temp_cif)
    else:
        temp_cif.rename(cif_output)
    
    return structure

def cif_to_xyz(structure, output_file="xyz.xyz"):
    # Convert output_file to Path if needed
    if isinstance(output_file, Path):
        output_path = output_file
    else:
        output_path = Path(output_file)
    
    xyz = XYZ(structure)
    xyz.write_file(str(output_path))  # Convert to string for write_file
    return xyz

if __name__ == '__main__':
    input_cif = '1525235.cif'
    matrix = (3, 3, 3)  # Should be tuple, not string
    output_cif = 'result.cif'
    make_supercell(input_cif, (1.0, 1.0, 1.0), matrix, output_cif, {})