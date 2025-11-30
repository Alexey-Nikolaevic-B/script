import os
import subprocess

def generate_lammps_script(template_lammps_path, run_dir, element1, element2, data_file, 
                          library_file, cross_potential_file, cohesive_e1, cohesive_e2):
    with open(template_lammps_path, 'r') as f:
        template = f.read()

    template = template.replace('{Timestep}', '{{Timestep}}')
    template = template.replace('{Temperature}', '{{Temperature}}')
    
    script = template.format(
        ELEMENT1_NUMBER=f"{element1}1",
        ELEMENT2_NUMBER=f"{element2}2",
        ELEMENT1=element1,
        ELEMENT2=element2,
        DATA_FILE=data_file,
        LIBRARY_FILE=library_file,
        CROSS_POTENTIAL_FILE=cross_potential_file,
        COHESIVE_E1=cohesive_e1,
        COHESIVE_E2=cohesive_e2
    )

    script = script.replace('{{Timestep}}', '{Timestep}')
    script = script.replace('{{Temperature}}', '{Temperature}')
    
    output_path = os.path.join(run_dir, 'formation.lmp')
    with open(output_path, 'w') as f:
        f.write(script)
    
    return output_path

def run_lammps_simulation(run_dir, lammps_executable):
    lammps_file = os.path.join(run_dir, 'formation.lmp')
    print(f"🚀 Running: {os.path.basename(lammps_file)}")
    
    try:
        result = subprocess.Popen(
            ["lmp", "-in", "formation.lmp"],
            cwd=run_dir,
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        return True
    except:
        return False
    

def simulate(template_lammps_path, element1, element2, run_dir):
    os.makedirs(run_dir, exist_ok=True)
    
    lammps_script = generate_lammps_script(
        template_lammps_path=template_lammps_path,
        run_dir=run_dir,
        element1=element1,
        element2=element2,
        data_file='CoTa2.data',
        library_file='library.meam', 
        cross_potential_file='CoTa.meam',
        cohesive_e1=-3.7,
        cohesive_e2=-8.1
    )
    
    print(f"✅ Generated: {lammps_script}")
    run_lammps_simulation(run_dir, "lmp")

if __name__ == "__main__":
    template_lammps_path = './template_formation.txt'
    element1 = 'Co'
    element2 = 'Ta'
    run_dir = f'./{element2}_{element1}/lammps'
    
    os.makedirs(run_dir, exist_ok=True)
    
    lammps_script = generate_lammps_script(
        template_lammps_path=template_lammps_path,
        run_dir=run_dir,
        element1=element1,
        element2=element2,
        data_file='CoTa2.data',
        library_file='library.meam', 
        cross_potential_file='CoTa.meam',
        cohesive_e1=-3.7,
        cohesive_e2=-8.1
    )
    
    print(f"✅ Generated: {lammps_script}")
    run_lammps_simulation(run_dir, "lmp")