import pandas as pd
import os
import glob

def get_meta_data(path):
    df = pd.read_excel(path)

    parsed_data = []
    for idx, row in df.iterrows():
        row_dict = row.to_dict()
        
        # Получаем элементы из колонок major и minor
        original_major = row_dict.get('major', '')
        original_minor = row_dict.get('minor', '')
        prototype_major = row_dict.get('prototype major', '')
        prototype_minor = row_dict.get('prototype minor', '')
        
        # Создаем строку элементов для отображения (без цифр)
        if original_major and original_minor:
            # Убираем цифры из названий элементов
            major_clean = ''.join([char for char in str(original_major) if not char.isdigit()])
            minor_clean = ''.join([char for char in str(original_minor) if not char.isdigit()])
            row_dict['elements_parsed'] = f"{major_clean} {minor_clean}"
        else:
            row_dict['elements_parsed'] = ""
        
        # Сохраняем major и minor элементы в нужном формате
        major_clean = ''.join([char for char in str(original_major) if not char.isdigit()]) if original_major else None
        minor_clean = ''.join([char for char in str(original_minor) if not char.isdigit()]) if original_minor else None
        proto_major_clean = ''.join([char for char in str(prototype_major) if not char.isdigit()]) if prototype_major else ''
        proto_minor_clean = ''.join([char for char in str(prototype_minor) if not char.isdigit()]) if prototype_minor else ''
        
        row_dict['major_element'] = [major_clean, proto_major_clean]
        row_dict['minor_element'] = [minor_clean, proto_minor_clean]
        
        lattice_params = ['a', 'b', 'c']
        for param in lattice_params:
            if param in row_dict:
                if pd.notna(row_dict[param]) and row_dict[param] not in ['', 'None', None]:
                    row_dict[param] = str(row_dict[param])
                else:
                    row_dict[param] = ""
        
        if 'prototype' in row_dict and pd.notna(row_dict['prototype']):
            prototype_str = str(row_dict['prototype'])
            if not prototype_str.endswith('.cif'):
                row_dict['prototype'] = prototype_str + '.cif'
        
        parsed_data.append(row_dict)
    
    return parsed_data


def delete_all_files(folder_path):
    """Delete all files in folder but keep the folder itself"""
    if not os.path.exists(folder_path):
        print(f"Folder does not exist: {folder_path}")
        return
    
    files = glob.glob(os.path.join(folder_path, "*"))
    deleted_count = 0
    
    for file_path in files:
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                deleted_count += 1
                print(f"✓ Deleted: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"✗ Error deleting {file_path}: {e}")
    
    print(f"Deleted {deleted_count} files from {folder_path}")