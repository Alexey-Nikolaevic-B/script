import subprocess
import os
import pandas as pd
import re
import time
import json
import pyautogui
from pathlib import Path

from input_capture import start_recording
from controls import hover_and_click, click, input_text, read, press_key, get_position_by_image, hover_only

def get_meta_data(path):
    df = pd.read_excel(path)
    
    def parse_elements(elements_str):
        """Парсит строку с элементами, убирая цифры из названий элементов"""
        if pd.isna(elements_str):
            return []
        
        elements = []
        # Разделяем по пробелам и парсим каждый элемент
        for elem_part in str(elements_str).split():
            elem_part = elem_part.strip()
            # Убираем цифры из названия элемента (Ta2 -> Ta, Co -> Co)
            element_name = ''.join([char for char in elem_part if not char.isdigit()])
            if element_name:  # Если осталось непустое название
                elements.append((element_name, 1))  # Всегда count=1, так как цифры убраны
        
        return elements
    
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

def open_vesta(vesta_path, cif_file):
    if os.path.exists(vesta_path) and os.access(vesta_path, os.X_OK):
        command = [vesta_path]
        command.append(cif_file)
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return process

def close_vesta():
    try:
        pyautogui.hotkey('ctrl', 'q')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        return True
        
    except Exception as e:
        print(f"Ошибка при закрытии VESTA: {e}")
        return False

def play_scenario(item):
    """Функция воспроизведения сценария для конкретного сплава"""
    click(position=[140, 74], hover_time=0.5)
    hover_and_click(position=[174, 145], speed=10.0, hover_time=0.2)
    hover_and_click(position=[426, 146], speed=10.0, hover_time=0.2)
    click(position=[1015, 605], hover_time=0.0, number=3, sleep=0.01)
    input_text(str(item['name']))

    click(position=[1049, 539], hover_time=0.0, number=1, sleep=0.05)

    # Change lattice params:
    if item.get('a'):
        click(position=[1146, 969], hover_time=0.0, number=1, sleep=0.05)
        input_text(str(item.get('a', '')))
    if item.get('b'):
        click(position=[1233, 962], hover_time=0.0, number=1, sleep=0.05)
        input_text(str(item.get('b', '')))
    if item.get('c'):
        click(position=[1281, 962], hover_time=0.0, number=1, sleep=0.05)
        input_text(str(item.get('c', '')))

    click(position=[1189, 521], hover_time=0.0, number=1, sleep=0.05)

    # Change lattice names:
    # первое поле
    click(position=[996, 811], hover_time=0.0, number=3, sleep=0.01)
    current_text = read()
    if current_text == item['major_element'][1]:
        input_text(str(item['major_element'][0]))
    elif current_text == item['minor_element'][1]:
        input_text(str(item['minor_element'][0]))
    # второе поле  
    click(position=[1052, 811], hover_time=0.0, number=3, sleep=0.01)
    current_text = read()
    if current_text == item['major_element'][1]:
        input_text(str(item['major_element'][0]))
    elif current_text == item['minor_element'][1]:
        input_text(str(item['minor_element'][0]))
    # третье поле
    click(position=[991, 830], hover_time=0.0, number=3, sleep=0.01)
    current_text = read()
    if current_text == item['major_element'][1]:
        input_text(str(item['major_element'][0]))
    elif current_text == item['minor_element'][1]:
        input_text(str(item['minor_element'][0]))
    # четвертое поле
    click(position=[1039, 832], hover_time=0.0, number=3, sleep=0.01)
    current_text = read()
    if current_text == item['major_element'][1]:
        input_text(str(item['major_element'][0]))
    elif current_text == item['minor_element'][1]:
        input_text(str(item['minor_element'][0]))

    click(position=[1049, 539], hover_time=0.0, number=1, sleep=0.05)

    click(position=[1093, 857], hover_time=0.0, number=1, sleep=0.05)

    # Supercell
    click(position=[950, 652], hover_time=0.0, number=1, sleep=0.05)
    input_text('2')
    click(position=[995, 683], hover_time=0.0, number=1, sleep=0.05)
    input_text('2')
    click(position=[1061, 732], hover_time=0.0, number=1, sleep=0.05)
    input_text('2')

    click(position=[1355, 958], hover_time=0.0, number=1, sleep=0.05)
    click(position=[1526, 818], hover_time=0.0, number=1, sleep=0.05)
    click(position=[1526, 818], hover_time=0.0, number=1, sleep=0.05)
    click(position=[1308, 842], hover_time=0.0, number=1, sleep=0.05)
    click(position=[1432, 1084], hover_time=0.0, number=1, sleep=0.05)

    press_key('ctrl', 'shift', 's')
    save_path = f"{item.get('name')}"
    click(position=[1316, 330], hover_time=0.0, number=1, sleep=0.05)
    click(position=[1306, 390], hover_time=0.0, number=2, sleep=0.05)
    input_text(save_path)
    press_key('enter')
    press_key('ctrl', 'q')

if __name__ == "__main__":
    create_recording = True

    element = 'Ta_Co'
    meta_data_path = f"./{element}/meta.xlsx"
    meta_data = get_meta_data(meta_data_path)
    
    print("=== PARSED DATA ===")
    for idx, item in enumerate(meta_data):
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

    vesta_path = "./VESTA-gtk3/VESTA"

    for item in meta_data:
        print(f"Processing {item.get('alloy')}...")
        
        prototype_file = item.get('prototype', '')

        cif_file = f"./{element}/cif/{prototype_file}"
    
        vesta_process = open_vesta(vesta_path, cif_file)
        time.sleep(2)

        play_scenario(item)