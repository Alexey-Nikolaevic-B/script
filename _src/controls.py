import pyautogui
import pyperclip
import time
from typing import List, Tuple, Optional

def click(position: Tuple[int, int], hover_time=0.0, number=1, sleep=0.1) -> bool:
    for x in range(number):
        try:
            pyautogui.moveTo(position[0], position[1])
            time.sleep(hover_time)
            pyautogui.click(position[0], position[1])
        except Exception as e:
            return False
        time.sleep(sleep)  
    return True

def press_key(*keys: str) -> bool:
    try:
        pyautogui.hotkey(*keys)
        return True
    except Exception as e:
        return False

def read() -> str:
    try:
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.01)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.01)
        text = pyperclip.paste()
        return text
    except Exception as e:
        return ""

def input_text(text: str, clear_field: bool = True) -> bool:
    try:
        if clear_field:
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.01)
            pyautogui.press('backspace')
            time.sleep(0.01)
        
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
        return True
    except Exception as e:
        return False

def hover_only(position: Tuple[int, int], speed: float = 1.0, hover_time: float = 1.0) -> bool:
    try:
        current_x, current_y = pyautogui.position()
        distance = max(abs(position[0] - current_x), abs(position[1] - current_y))
        steps = max(int(distance / 2), 10)
        duration = steps * 0.01 / speed
        
        pyautogui.moveTo(position[0], position[1], duration=duration)
        time.sleep(hover_time)
        return True
    except Exception as e:
        return False