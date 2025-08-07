from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def submit_simple_form(driver, message):
    driver.get("https://www.lambdatest.com/selenium-playground/simple-form-demo")

    message_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//input[@id="user-message"]'))
    )
    message_box.send_keys(message)

    with open("D:\programming coding\codi VS учеба\Py seleniym/log.txt", "a") as file:
        file.write("Success write message\n")

    show_message_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//Button[@id="showInput"]'))
    )
    show_message_button.click()

    with open("D:\programming coding\codi VS учеба\Py seleniym/log.txt", "a") as file:
        file.write("Success click show message\n")

    displayed_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'message'))
    )
    print("Displayed Message: ", displayed_message.text)

if __name__ == "__main__":
    driver = webdriver.Firefox()
    try:
        submit_simple_form(driver, "Hello, this is a test message.")
    except Exception as e:
        print(f"Ошибка в процессе выполнения: {e}")
    finally:
        time.sleep(15)
        driver.quit()
