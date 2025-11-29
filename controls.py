import pyautogui
import pyperclip
import time
from typing import List, Tuple, Optional

# ==================== ОСНОВНЫЕ ФУНКЦИИ ====================

def hover_and_click(position: Tuple[int, int], 
                   speed: float = 1.0, 
                   hover_time: float = 0.5) -> bool:
    """
    Плавно наводится на позицию и кликает
    """
    try:
        current_x, current_y = pyautogui.position()
        distance = max(abs(position[0] - current_x), abs(position[1] - current_y))
        steps = max(int(distance / 2), 10)
        duration = steps * 0.01 / speed
        
        pyautogui.moveTo(position[0], position[1], duration=duration)
        time.sleep(hover_time)
        pyautogui.click()
        return True
        
    except Exception as e:
        print(f"Ошибка в hover_and_click: {e}")
        return False

def click(position: Tuple[int, int], hover_time=0.0, number=1, sleep=0.1) -> bool:
    """
    Кликает по позиции
    """
    for x in range(number):
        try:
            pyautogui.moveTo(position[0], position[1])
            time.sleep(hover_time)
            pyautogui.click(position[0], position[1])
        except Exception as e:
            print(f"Ошибка в click: {e}")
            return False
        time.sleep(sleep)  
    return True

def press_key(*keys: str) -> bool:
    """
    Нажимает комбинацию горячих клавиш
    """
    try:
        pyautogui.hotkey(*keys)
        return True
    except Exception as e:
        print(f"Ошибка в hot_key {keys}: {e}")
        return False

def read() -> str:
    """
    Получает текст из ячейки по указанной позиции
    """
    try:
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.01)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.01)
        text = pyperclip.paste()
        return text
        
    except Exception as e:
        return False

def input_text(text: str, clear_field: bool = True) -> bool:
    """
    Вводит текст, предварительно очищая поле
    """
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
        print(f"Ошибка в input_text: {e}")
        return False

def get_position_by_image(image_path: str, 
                         confidence: float = 0.8,
                         timeout: float = 10.0) -> Optional[Tuple[int, int]]:
    """
    Находит координаты элемента по изображению
    """
    try:
        start_time = time.time()
        while time.time() - start_time < timeout:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center_x = location.left + location.width // 2
                center_y = location.top + location.height // 2
                return (center_x, center_y)
            time.sleep(0.5)
        
        print(f"Элемент не найден: {image_path}")
        return None
        
    except Exception as e:
        print(f"Ошибка поиска изображения {image_path}: {e}")
        return None

def hover_only(position: Tuple[int, int], 
              speed: float = 1.0,
              hover_time: float = 1.0) -> bool:
    """
    Только наведение без клика
    """
    try:
        current_x, current_y = pyautogui.position()
        distance = max(abs(position[0] - current_x), abs(position[1] - current_y))
        steps = max(int(distance / 2), 10)
        duration = steps * 0.01 / speed
        
        pyautogui.moveTo(position[0], position[1], duration=duration)
        time.sleep(hover_time)
        return True
        
    except Exception as e:
        print(f"Ошибка в hover_only: {e}")
        return False

# ==================== ФУНКЦИИ ДЛЯ ПОЛЕЙ ВВОДА ====================

def get_input_field_by_label(label_image: str, 
                           offset_x: int = 0, 
                           offset_y: int = 30,
                           confidence: float = 0.8) -> Optional[Tuple[int, int]]:
    """
    Находит поле ввода по метке над ним
    """
    label_position = get_position_by_image(label_image, confidence=confidence)
    if not label_position:
        print(f"Метка не найдена: {label_image}")
        return None
    
    field_x = label_position[0] + offset_x
    field_y = label_position[1] + offset_y
    print(f"Найдено поле по метке '{label_image}': ({field_x}, {field_y})")
    return (field_x, field_y)

def get_input_fields_by_template(field_template: str, 
                               expected_count: int = None,
                               confidence: float = 0.7) -> List[Tuple[int, int]]:
    """
    Находит все похожие поля ввода
    """
    all_fields = []
    
    try:
        locations = pyautogui.locateAllOnScreen(field_template, confidence=confidence)
        for location in locations:
            center_x = location.left + location.width // 2
            center_y = location.top + location.height // 2
            all_fields.append((center_x, center_y))
        
        all_fields.sort(key=lambda pos: pos[1])
        print(f"Найдено полей: {len(all_fields)}")
        
        if expected_count and len(all_fields) != expected_count:
            print(f"Внимание: ожидалось {expected_count} полей, найдено {len(all_fields)}")
        
        return all_fields
        
    except Exception as e:
        print(f"Ошибка поиска полей: {e}")
        return []

def get_nth_input_field(field_template: str, 
                       index: int, 
                       confidence: float = 0.7) -> Optional[Tuple[int, int]]:
    """
    Получает поле ввода по порядковому номеру
    """
    fields = get_input_fields_by_template(field_template, confidence=confidence)
    if len(fields) > index:
        print(f"Найдено поле #{index} на позиции: {fields[index]}")
        return fields[index]
    else:
        print(f"Поле #{index} не найдено. Всего полей: {len(fields)}")
        return None

def get_specific_input_field(label_image: str,
                           field_template: str,
                           search_region_height: int = 100,
                           confidence: float = 0.7) -> Optional[Tuple[int, int]]:
    """
    Находит поле по метке и шаблону
    """
    label_position = get_position_by_image(label_image, confidence=confidence)
    if not label_position:
        return None
    
    label_x, label_y = label_position
    search_region = (label_x - 50, label_y + 10, 300, search_region_height)
    
    try:
        location = pyautogui.locateOnScreen(field_template, confidence=confidence, region=search_region)
        if location:
            center_x = location.left + location.width // 2
            center_y = location.top + location.height // 2
            print(f"Найдено поле '{label_image}': ({center_x}, {center_y})")
            return (center_x, center_y)
    except Exception as e:
        print(f"Ошибка поиска поля: {e}")
    
    return None

# ==================== ФУНКЦИИ-ОБЕРТКИ ДЛЯ ЗАПОЛНЕНИЯ ====================

def fill_field_by_label(label_image: str, 
                       text: str, 
                       offset_y: int = 30,
                       clear_field: bool = True,
                       click_delay: float = 0.2) -> bool:
    """
    Находит поле по метке и заполняет его
    """
    position = get_input_field_by_label(label_image, offset_y=offset_y)
    if not position:
        return False
    
    time.sleep(click_delay)
    click(position)
    time.sleep(click_delay)
    input_text(text, clear_field=clear_field)
    return True

def fill_nth_field(field_template: str, 
                  index: int, 
                  text: str,
                  clear_field: bool = True,
                  click_delay: float = 0.2) -> bool:
    """
    Заполняет поле по порядковому номеру
    """
    position = get_nth_input_field(field_template, index)
    if not position:
        return False
    
    time.sleep(click_delay)
    click(position)
    time.sleep(click_delay)
    input_text(text, clear_field=clear_field)
    return True

def fill_field_advanced(label_image: str,
                       field_template: str,
                       text: str,
                       clear_field: bool = True,
                       click_delay: float = 0.2) -> bool:
    """
    Заполняет поле используя комбинированный поиск
    """
    position = get_specific_input_field(label_image, field_template)
    if not position:
        return False
    
    time.sleep(click_delay)
    click(position)
    time.sleep(click_delay)
    input_text(text, clear_field=clear_field)
    return True

# ==================== ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ====================

def example_fill_registration_form():
    """Пример заполнения регистрационной формы"""
    # Заполняем поля по меткам
    fill_field_by_label("username_label.png", "john_doe", offset_y=35)
    fill_field_by_label("password_label.png", "secure_pass", offset_y=35)
    fill_field_by_label("email_label.png", "john@example.com", offset_y=30)

def example_fill_dynamic_form():
    """Пример заполнения полей по порядку"""
    fill_nth_field("input_field_template.png", 0, "Значение 1")
    fill_nth_field("input_field_template.png", 1, "Значение 2") 
    fill_nth_field("input_field_template.png", 2, "Значение 3")

def example_complex_workflow():
    """Пример сложного workflow"""
    # Находим и кликаем на меню
    menu_pos = get_position_by_image("menu_button.png")
    if menu_pos:
        hover_and_click(menu_pos, speed=0.8, hover_time=0.3)
    
    # Заполняем форму
    fill_field_by_label("name_label.png", "Иван Иванов")
    fill_field_by_label("phone_label.png", "+79991234567")
    
    # Нажимаем кнопку отправки
    submit_pos = get_position_by_image("submit_button.png")
    if submit_pos:
        click(submit_pos)

def example_manual_field_processing():
    """Пример ручной работы с полями"""
    # Получаем все поля
    all_fields = get_input_fields_by_template("input_field.png")
    
    # Заполняем каждое поле
    for i, field_pos in enumerate(all_fields):
        print(f"Заполняем поле {i+1}")
        click(field_pos)
        input_text(f"Текст для поля {i+1}")
        time.sleep(0.5)

# ==================== ЗАПУСК ПРИМЕРОВ ====================

if __name__ == "__main__":
    # Настройка безопасности
    pyautogui.FAILSAFE = True
    
    # Пример использования
    print("Запуск автоматизации...")
    
    # Даем время переключиться на нужное окно
    time.sleep(3)
    
    # Запускаем нужный пример
    example_fill_registration_form()
    
    print("Автоматизация завершена!")