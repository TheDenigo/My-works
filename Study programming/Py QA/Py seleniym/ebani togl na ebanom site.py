import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.service import Service

# Путь к драйверу
service = Service('D:\\programming coding\\codi VS учеба\\Py seleniym\\geckodriver.exe')
driver = webdriver.Firefox(service=service)

# Проверка соединения с сайтом
url = 'https://demoqa.com/checkbox'
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Проверяет, был ли успешным запрос
    print("Соединение с сайтом успешно.")

    # Переход на страницу
    driver.get(url)

    
    wait = WebDriverWait(driver, 10)
    button_xpath = '//*[@id="tree-node"]/ol/li/span/button'

    # Проверяем наличие элемента
    element = wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))

    # Проверяем, виден ли элемент
    if element.is_displayed():
        print("Тогл виден, выполняем клик.")
        element.click()  # Клик по элементу
    else:
        print("Тогл не виден, не выполняем клик.")

except requests.exceptions.RequestException as e:
    print(f"Не удалось подключиться к сайту: {e}")

except TimeoutException:
    print("Тогл не найден за отведённое время.")

except NoSuchElementException:
    print("Элемент с указанным XPath не найден.")

except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    driver.quit()