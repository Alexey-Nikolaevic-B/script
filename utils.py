import pandas as pd
import os
import glob

def get_meta_data(path):
    df = pd.read_excel(path)
    parsed_data = []
    
    for idx, row in df.iterrows():
        row_dict = row.to_dict()
        
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
                    row_dict[param] = str(row_dict[param])
                else:
                    row_dict[param] = ""
        
        if 'cif_file' in row_dict and pd.notna(row_dict['cif_file']):
            cif_str = str(row_dict['cif_file'])
            if not cif_str.endswith('.cif'):
                row_dict['cif_file'] = cif_str + '.cif'
        
        parsed_data.append(row_dict)
    
    return parsed_data

def delete_all_files(folder_path):
    if not os.path.exists(folder_path):
        return
    
    files = glob.glob(os.path.join(folder_path, "*"))
    
    for file_path in files:
        if os.path.isfile(file_path):
            os.remove(file_path)