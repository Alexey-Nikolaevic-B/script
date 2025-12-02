import time
import json
import pyautogui

from datetime import datetime
from pynput import mouse, keyboard

actions = []
recording = False
start_time = None
mouse_listener = None
keyboard_listener = None
output_filename = None

# Конфигурация горячих клавиш
config = {
    'click_shortcut': None,
    'input_text_shortcut': None,
    'stop_recording': None
}

def on_click(x, y, button, pressed):
    if pressed and recording:
        timestamp = time.time() - start_time
        action = {
            'type': 'click',
            'x': x,
            'y': y,
            'button': str(button),
            'timestamp': round(timestamp, 2)
        }
        actions.append(action)
        

def on_key_press(key):
    if not recording:
        return
        
    timestamp = time.time() - start_time
    
    # Остановка записи
    if key == config['stop_recording']:
        stop_recording()
        return
    
    # Горячая клавиша для click команды
    if key == config['click_shortcut']:
        current_x, current_y = pyautogui.position()
        command = f"click(position=[{current_x}, {current_y}], hover_time=0.0, number=1, sleep=0.05)"
        actions.append({
            'type': 'click_shortcut',
            'x': current_x,
            'y': current_y,
            'timestamp': round(timestamp, 2)
        })
        print(command)
        return
    
    # Горячая клавиша для input_text команды
    if key == config['input_text_shortcut']:
        command = "input_text('')"
        actions.append({
            'type': 'empty_input',
            'timestamp': round(timestamp, 2)
        })
        print(command)
        return

def start_recording(filename, settings):
    global actions, recording, start_time, mouse_listener, keyboard_listener, output_filename
    
    # Устанавливаем конфигурацию
    config.update(settings)
    
    output_filename = filename
    actions = []
    recording = True
    start_time = time.time()
    
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()
    
    keyboard_listener = keyboard.Listener(on_press=on_key_press)
    keyboard_listener.start()
    
    print("Recording started!")
    print(f"Press {config['stop_recording']} to stop recording.")
    print(f"{config['click_shortcut']} - outputs click command at current mouse position")
    print(f"{config['input_text_shortcut']} - outputs empty input_text command")
    
    while recording:
        time.sleep(0.1)
        
    mouse_listener.stop()
    keyboard_listener.stop()

def stop_recording():
    global recording
    recording = False
    save_actions()

def get_actions():
    return actions.copy()

def save_actions():
    if not output_filename:
        return None
    
    data = {
        'recorded_at': datetime.now().isoformat(),
        'total_actions': len(actions),
        'actions': actions
    }
    
    with open(output_filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nActions saved to: {output_filename}")
    return output_filename

import os
import subprocess
def open_vesta(vesta_path, cif_file):
    if os.path.exists(vesta_path) and os.access(vesta_path, os.X_OK):
        command = [vesta_path]
        command.append(cif_file)
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return process

if __name__ == "__main__":
    settings = {
        'click_shortcut': keyboard.Key.num_lock,  # Fn клавиша
        'input_text_shortcut': keyboard.Key.shift,  # Shift
        'stop_recording': keyboard.Key.esc  # Esc
    }
    

    vesta_path = "./VESTA-gtk3/VESTA"
    cif_file = './Ta_Co/cif/9012196.cif'
    open_vesta(vesta_path, cif_file)

    start_recording(
        filename="recorded_actions.json",
        settings=settings
    )


