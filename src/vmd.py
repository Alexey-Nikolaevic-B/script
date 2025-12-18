import os
import subprocess
import math

def create_vmd_script(xyz_path, output_dir, lattice_a, lattice_b, lattice_c):
    data_file = os.path.basename(xyz_path).replace('.xyz', '.data')
    script = f"""#!/usr/bin/vmd
mol new "{xyz_path}" type xyz
cd "{output_dir}"

molinfo top set a {lattice_a}
molinfo top set b {lattice_b}
molinfo top set c {lattice_c}
molinfo top set alpha 90.0
molinfo top set beta 90.0
molinfo top set gamma 90.0

topo writelammpsdata "{data_file}" full
quit
"""
    return script

def execute_vmd(script_path):
    subprocess.run(['vmd', '-e', script_path], capture_output=True, text=True, check=True)
    return True

def xyz_to_data(xyz_path, output_dir, script_name, lattice_a, lattice_b, lattice_c, supercell_size):
    os.makedirs(output_dir, exist_ok=True)
    
    lattice_a, lattice_b, lattice_c = caluclaue_new_size(lattice_a, lattice_b, lattice_c, supercell_size)

    script_content = create_vmd_script(xyz_path, output_dir, lattice_a, lattice_b, lattice_c)
    script_path = os.path.join(output_dir, script_name)
    
    with open(script_path, 'w') as f:
        f.write(script_content)
    os.chmod(script_path, 0o755)
    
    execute_vmd(script_path)

def caluclaue_new_size(lattice_a, lattice_b, lattice_c, supercell_size):
    new_lattice_a = round_value(lattice_a * supercell_size)
    new_lattice_b = round_value(lattice_b * supercell_size)
    new_lattice_c = round_value(lattice_c * supercell_size)
    
    return new_lattice_a, new_lattice_b, new_lattice_c

def round_value(value):
    return math.ceil(value * 10) / 10