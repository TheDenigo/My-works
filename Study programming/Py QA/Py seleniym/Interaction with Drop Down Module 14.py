from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time


# Инициализация драйвера (пример для Chrome)
def setup():
    driver = webdriver.Edge()
    return driver

# ... Код для входа в систему (логин и пароль) ...
def login(driver, username, password):
    driver.get('https://www.saucedemo.com/') # Переход на страницу входа
    driver.find_element(By.ID, 'user-name').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'login-button').click()


if __name__ == "__main__":
    driver = setup()
    try:
        login(driver, "standard_user", "secret_sauce")
        print("Real login test passed.")

        time.sleep(6)

        # Находим элемент select
        select = Select(driver.find_element(By.XPATH, value='//*[@id="header_container"]/div[2]/div/span/select'))

        # Выбираем опцию по видимому тексту
        select.select_by_visible_text("Price (low to high)")

        time.sleep(2)

        # Находим кликабельный элемент для открытия drop-down
        click_drop = driver.find_element(By.XPATH, value='/html/body/div/div/div/div[1]/div[2]/div/span')
        click_drop.click()
        time.sleep(6)

        # Находим поле ввода внутри drop-down
        click_form = driver.find_element(By.XPATH, value='/html/body/div/div/div/div[1]/div[2]/div/span/select')
        click_form.send_keys('low to high')
        time.sleep(5)

        # Добавляем Enter
        click_form.send_keys(Keys.ENTER)

        time.sleep(5)
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        if driver:
            driver.quit()