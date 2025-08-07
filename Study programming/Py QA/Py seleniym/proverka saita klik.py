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
url = 'https://www.lambdatest.com/selenium-playground/simple-form-demo'
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Проверяет, был ли успешным запрос
    print("Соединение с сайтом успешно.")

    # Переход на страницу
    driver.get(url)

    input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'user-message'))
    )
    input_field.send_keys('Hello from Firefox!')
    
    # Явное ожидание элемента по XPath
    wait = WebDriverWait(driver, 10)  # Ожидаем до 10 секунд
    button_xpath = '//*[@id="showInput"]'  # XPath кнопки

    # Проверяем наличие кнопки
    button = wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))

    # Проверяем, видима ли кнопка
    if button.is_displayed():
        print("Кнопка видима, выполняем клик.")
        button.click()  # Клик по кнопке

        # Проверяем, удалось ли кликнуть (замените это на логику, соответствующую вашему случаю)
        # Например, проверим изменение текста кнопки или наличие элемента после клика
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, button_xpath), "Новый текст после клика"))
        print("Клик выполнен успешно.")
    else:
        print("Кнопка не видима, клик не выполнен.")

except requests.exceptions.RequestException as e:
    print(f"Не удалось подключиться к сайту: {e}")

except TimeoutException:
    print("Кнопка не найдена за отведённое время.")

except NoSuchElementException:
    print("Элемент с указанным XPath не найден.")

except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    driver.quit()  # Закрыть браузер