from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Инициализируем веб-драйвер
driver = webdriver.Edge()

try:
    # Открываем нужный сайт
    driver.get("https://demoqa.com/radio-button")
    print("Открыта страница: https://demoqa.com/radio-button")

    time.sleep(3)

    # Явное ожидание и клик по label радиокнопки "Yes"
    yes_radio_label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//label[@for="yesRadio"]')) #/html/body/div[2]/div/div/div/div[2]/div[2]/div[2]/label
    )
    yes_radio_label.click()
    print("Кликнули на радиокнопку 'Yes'")

    # Проверка, что радиокнопка "Yes" выбрана
    yes_radio_input = driver.find_element(By.XPATH, '//input[@id="yesRadio"]')
    if yes_radio_input.is_selected():
         print("Радиокнопка 'Yes' выбрана")
    else:
         print("Радиокнопка 'Yes' не выбрана")

    time.sleep(2)

    # Аналогично для радиокнопки "Impressive"
    impressive_radio_label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//label[@for="impressiveRadio"]'))
    )
    impressive_radio_label.click()
    print("Кликнули на радиокнопку 'Impressive'")

    impressive_radio_input = driver.find_element(By.XPATH, '//input[@id="impressiveRadio"]')
    if impressive_radio_input.is_selected():
        print("Радиокнопка 'Impressive' выбрана")
    else:
        print("Радиокнопка 'Impressive' не выбрана")


    # задержка перед закрытием
    time.sleep(3)

finally:
    # Закрываем браузер
    driver.quit()
    print("Браузер закрыт")
