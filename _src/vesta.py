import subprocess
import os
import time
from _src.controls import click, input_text, press_key

def launch_vesta(vesta_path, cif_file):
    command = [vesta_path, cif_file]
    return subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def open_edit_data():
    press_key('ctrl', 'e')

def set_alloy_name(name):
    click(position=[1015, 605], number=3)
    input_text(name)

def adjust_lattice(a, b, c):
    click(position=[1049, 539])
    if a:
        click(position=[1146, 969])
        input_text(a)
    click(position=[1347, 752])
    if b:
        click(position=[1233, 962])
        input_text(b)
    click(position=[1347, 752])
    if c:
        click(position=[1281, 962])
        input_text(c)

def create_supercell(size):
    click(position=[1120, 859])
    click(position=[950, 652])
    input_text(size)
    click(position=[995, 683])
    input_text(size)
    click(position=[1061, 732])
    input_text(size)

def export_file(path):
    click(position=[1355, 958])
    click(position=[1526, 818], number=2)
    click(position=[1308, 842])
    click(position=[1432, 1084])

    click(position=[87, 72])
    click(position=[174, 248])
    click(position=[1902, 1187])
    click(position=[1857, 1380])

    click(position=[1316, 330])
    input_text(path)
    time.sleep(0.9)
    press_key('enter')
    time.sleep(0.9)
    press_key('enter')
    click(position=[1306, 190], number=2)
    press_key('ctrl', 'q')
    time.sleep(0.1)
    click(position=[1344, 779])

def update_elements(file_path, major_new, major_old, minor_new, minor_old):
    full_path = f"./Ta_Co/{file_path}.xyz"
    
    with open(full_path, 'r') as f:
        content = f.read()
    
    if major_old and major_new:
        content = content.replace(major_old, major_new)
    if minor_old and minor_new:
        content = content.replace(minor_old, minor_new)
    
    with open(full_path, 'w') as f:
        f.write(content)
