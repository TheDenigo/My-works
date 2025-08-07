from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service('D:\programming coding\codi VS учеба\Py seleniym\geckodriver.exe')
driver = webdriver.Firefox(service=service)

try:
    driver.get('https://www.lambdatest.com/selenium-playground/simple-form-demo')

    input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'user-message'))
    )
    input_field.send_keys('Hello from Firefox!')

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'showInput'))
    )
    button.click()

    time.sleep(15)
finally:
    driver.quit()