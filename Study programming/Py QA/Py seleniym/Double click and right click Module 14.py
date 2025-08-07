from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time


# Инициализируем веб-драйвер
driver = webdriver.Edge()

try:
    # Открываем страницу с кнопками
    driver.get("https://demoqa.com/buttons")
    print("Открыта страница: https://demoqa.com/buttons")

    # 1. Поиск кнопок
    double_click_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="doubleClickBtn"]'))
    )
    right_click_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="rightClickBtn"]'))
    )
    standard_click_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Click Me"]'))
    )

    # 2. Создание экземпляра ActionChains
    action = ActionChains(driver)

    # 3. Двойной клик
    action.double_click(double_click_button).perform()
    print("Выполнен двойной клик")

    # 4. Клик правой кнопкой мыши
    action.context_click(right_click_button).perform()
    print("Выполнен правый клик")

    # 5. Стандартный клик
    standard_click_button.click()
    print("Выполнен стандартный клик")

    # задержка перед закрытием
    time.sleep(3)

finally:
    # Закрываем браузер
    driver.quit()
    print("Браузер закрыт")