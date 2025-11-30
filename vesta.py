import subprocess
import os
import pandas as pd
import time

from controls import hover_and_click, click, input_text, read, press_key, get_position_by_image, hover_only

from utils import get_meta_data, delete_all_files

def open_vesta(vesta_path, cif_file):
    if os.path.exists(vesta_path) and os.access(vesta_path, os.X_OK):
        command = [vesta_path]
        command.append(cif_file)
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return process

def play_scenario(item, save_path):
    
    press_key('ctrl', 'e')
    click(position=[1015, 605], hover_time=0.0, number=3, sleep=0.01)
    input_text(str(item['name']))

    click(position=[1049, 539], hover_time=0.0, number=1, sleep=0.05)

    # Change lattice params:
    if item.get('a'):
        click(position=[1146, 969], hover_time=0.0, number=1, sleep=0.05)
        input_text(str(item.get('a', '')))
    click(position=[1347, 752], hover_time=0.0, number=1, sleep=0.05)
    if item.get('b'):
        click(position=[1233, 962], hover_time=0.0, number=1, sleep=0.05)
        input_text(str(item.get('b', '')))
    click(position=[1347, 752], hover_time=0.0, number=1, sleep=0.05)
    if item.get('c'):
        click(position=[1281, 962], hover_time=0.0, number=1, sleep=0.05)
        input_text(str(item.get('c', '')))

    click(position=[1189, 521], hover_time=0.0, number=1, sleep=0.05)

    # Change lattice names:
    click(position=[999, 814], hover_time=0.0, number=1, sleep=0.05)
    click(position=[1299, 618], hover_time=0.0, number=1, sleep=0.05)
    current_text = read()
    if current_text == item['major_element'][1]:
        element = str(item['major_element'][0])
    elif current_text == item['minor_element'][1]:
        element = str(item['minor_element'][0])

    click(position=[1299, 618], hover_time=0.0, number=1, sleep=0.05)
    input_text(element)
    click(position=[1414, 612], hover_time=0.0, number=1, sleep=0.05)
    input_text(element)


    click(position=[991, 830], hover_time=0.0, number=1, sleep=0.01)
    click(position=[1306, 612], hover_time=0.0, number=1, sleep=0.05)
    current_text = read()
    if current_text == item['major_element'][1]:
        element = str(item['major_element'][0])
    elif current_text == item['minor_element'][1]:
        element = str(item['minor_element'][0])

    click(position=[1306, 612], hover_time=0.0, number=1, sleep=0.05)
    input_text(element)
    click(position=[1405, 610], hover_time=0.0, number=1, sleep=0.05)
    input_text(element)


    # Supercell
    click(position=[1049, 539], hover_time=0.0, number=1, sleep=0.05)

    click(position=[1093, 857], hover_time=0.0, number=1, sleep=0.05)

    click(position=[950, 652], hover_time=0.0, number=1, sleep=0.05)
    input_text(item['super_cell'])
    click(position=[995, 683], hover_time=0.0, number=1, sleep=0.05)
    input_text(item['super_cell'])
    click(position=[1061, 732], hover_time=0.0, number=1, sleep=0.05)
    input_text(item['super_cell'])

    click(position=[1355, 958], hover_time=0.0, number=1, sleep=0.05)
    click(position=[1526, 818], hover_time=0.0, number=1, sleep=0.05)
    click(position=[1526, 818], hover_time=0.0, number=1, sleep=0.05)
    click(position=[1308, 842], hover_time=0.0, number=1, sleep=0.05)
    click(position=[1432, 1084], hover_time=0.0, number=1, sleep=0.05)

    click(position=[87, 72], hover_time=0.0, number=1, sleep=0.05)
    click(position=[174, 248], hover_time=0.0, number=1, sleep=0.05)
    click(position=[1902, 1187], hover_time=0.0, number=1, sleep=0.05)
    click(position=[1857, 1380], hover_time=0.0, number=1, sleep=0.05)

    click(position=[1316, 330], hover_time=0.0, number=1, sleep=0.05)
    input_text(save_path)
    time.sleep(0.9)
    press_key('enter')
    time.sleep(0.9)
    press_key('enter')
    click(position=[1306, 190], hover_time=0.0, number=2, sleep=0.05)
    press_key('ctrl', 'q')
    time.sleep(0.1)
    click(position=[1344, 779], hover_time=0.0, number=1, sleep=0.05)


def cif_to_xyz(vesta_path, cif_path, item, save_path):
    vesta_process = open_vesta(vesta_path, cif_path)
    time.sleep(2)
    play_scenario(item, save_path)


if __name__ == "__main__":

    element = 'Ta_Co'
    data_path = f"./{element}/data.xlsx"
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

    vesta_path = "./VESTA-gtk3/VESTA"

    delete_all_files(f'{element}/vesta')

    for item in data:
        print(f"Processing {item.get('name')}...")
        
        prototype_file = item.get('prototype', '')
        cif_file = f"./{element}/cif/{prototype_file}"
    
        vesta_process = open_vesta(vesta_path, cif_file)
        time.sleep(2)

        play_scenario(item)