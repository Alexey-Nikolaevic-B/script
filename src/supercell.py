#!/usr/bin/env python

import sys
import re
import os

from ase.io import read

from pymatgen.io.cif import CifParser
from pymatgen.io.lammps.data import LammpsData
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.io.cif import CifWriter

from pymatgen.core.structure import Structure
from pymatgen.core.lattice import Lattice
from pymatgen.io.xyz import XYZ

def make_supercell(cif_input, lattice_params, supercell_matrix, cif_output, element_mapping):
    structure = Structure.from_file(cif_input)
    
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
    
    structure.make_supercell(supercell_matrix, to_unit_cell=True)
    
    temp_cif = cif_output + ".temp"
    writer = CifWriter(structure)
    writer.write_file(temp_cif)
    
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
        os.rename(temp_cif, cif_output)
    
    return structure


def cif_to_xyz(structure, output_file="xyz.xyz"):
    xyz = XYZ(structure)
    xyz.write_file(output_file)
    return xyz

if __name__ == '__main__':

    input = '1525235.cif'
    matrix = "3, 3, 3"
    output = 'result.cif'
    make_supercell(input, matrix, output)
