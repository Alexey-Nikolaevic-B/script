import os
import subprocess

def generate_lammps_script(template_lammps_path, run_dir, element1, element2, data_file, 
                          library_file, cross_potential_file, cohesive_e1, cohesive_e2, dimension, n, m, coef):
    with open(template_lammps_path, 'r') as f:
        template = f.read()

    replacements = {
        '{ELEMENT1_NUMBER}': f"{element1}{n}",
        '{ELEMENT2_NUMBER}': f"{element2}{m}",
        '{ELEMENT1}': element1,
        '{ELEMENT2}': element2,
        '{DATA_FILE}': data_file,
        '{LIBRARY_FILE}': library_file,
        '{CROSS_POTENTIAL_FILE}': cross_potential_file,
        '{COHESIVE_E1}': str(cohesive_e1),
        '{COHESIVE_E2}': str(cohesive_e2),
        '{DIMENSION}': str(dimension),
        '{N_ELEMENT1}': str(n),
        '{M_ELEMENT2}': str(m),
        '{COEF}': str(coef)

    }
    
    for old, new in replacements.items():
        template = template.replace(old, new)
    
    output_path = os.path.join(run_dir, 'formation.lmp')
    with open(output_path, 'w') as f:
        f.write(template)
    
    return output_path


def run_lammps_simulation(run_dir, lammps_code):    
    try:
        result = subprocess.run(
            ["lmp", "-in", lammps_code],
            cwd=run_dir
        )
        return True
    except:
        return False
    

def simulate(template_lammps_path, element1, element2, run_dir, alloy_data, cross_potential_file, library_file, lammps_code, supercell, n, m, coef):
    lammps_script = generate_lammps_script(
        template_lammps_path=template_lammps_path,
        run_dir=run_dir,
        element1=element1,
        element2=element2,
        data_file=alloy_data,
        library_file='library.meam', 
        cross_potential_file=cross_potential_file,
        cohesive_e1=-4.41,
        cohesive_e2=-8.09, 
        dimension=supercell,
        n=n,
        m=m,
        coef=coef
    )
    
    try:
        run_lammps_simulation(run_dir, lammps_code)
        return True
    except:
        return False