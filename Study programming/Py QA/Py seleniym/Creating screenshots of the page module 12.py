import os
import time
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def create_screenshot(driver, scenario_name):

    print("Текущая рабочая директория:", os.getcwd())
    
    # Форматируем текущее время для имени файла
    timestamp = datetime.now().strftime("%H-%M-%S_%Y-%m-%d")
    
    # Создаем директорию для сценариев, если она не существует
    directory = f"screen/{scenario_name}"
    os.makedirs(directory, exist_ok=True)

    # Полный путь для сохранения скриншота
    screenshot_path = os.path.join(directory, f'screenshot_{timestamp}.png')

    # Сохраняем скриншот
    driver.save_screenshot(screenshot_path)
    print(f"Скриншот сохранен: {screenshot_path}")

def test_login():
    # Инициализируем драйвер (например, Chrome)
    driver = webdriver.Firefox()

    try:
        # Открываем веб-страницу
        driver.get("https://www.saucedemo.com/")

        # Пауза для загрузки страницы
        time.sleep(2)

        # Создаем скриншот после загрузки страницы
        create_screenshot(driver, "login_page")

        # Заполняем форму логина
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        username_input.send_keys("standard_user")
        
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_input.send_keys("secret_sauce")

        # Создаем скриншот после заполнения формы
        create_screenshot(driver, "filled_login_form")

        # Отправляем форму
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login-button"))
        )
        login_button.click()

        # Пауза для ожидания перехода на новую страницу
        time.sleep(15)

        # Создаем скриншот после входа в систему
        create_screenshot(driver, "after_login")

    finally:
        # Закрываем браузер
        driver.quit()

# Запуск теста
test_login()
