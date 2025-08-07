from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def login_with_enter(driver, username, password):
    driver.find_element(By.ID, 'user-name').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'password').send_keys(Keys.ENTER)

def sc_real_login_with_enter():
    driver = webdriver.Firefox()
    driver.get("https://www.saucedemo.com/")
    login_with_enter(driver, "standard_user", "secret_sauce")
    
    time.sleep(2)
    driver.quit()

sc_real_login_with_enter()