from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time
import os

def setup():
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.get("https://www.saucedemo.com/")
    return driver

def login(driver, username, password):
    driver.find_element(By.ID, 'user-name').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'login-button').click()

def test_fake_login_label(driver):
    correct_text = "Epic sadface: Username and password do not match any user in this service"
    error_message_element = driver.find_element(By.XPATH, '//*[contains(text(), "Epic sadface")]')
    current_text = error_message_element.text
  
    assert correct_text == current_text, "test_fake_login_label is Failed"
    with open(r'D:\programming coding\codi VS учеба\Py seleniym\test_results.txt', 'a') as file:
        file.write('test_fake_login_label is OK\n')

if __name__ == "__main__":
    driver = setup()
    try:
        login(driver, "standard_user", "fake_password")
        time.sleep(2)
        test_fake_login_label(driver)

        driver.get("https://www.saucedemo.com/")

        login(driver, "standard_user", "secret_sauce")
        print("Real login test passed.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        time.sleep(5)
        driver.quit()