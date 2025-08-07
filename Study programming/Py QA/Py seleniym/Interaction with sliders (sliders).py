from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# Инициализация драйвера (пример для Chrome)
driver = webdriver.Chrome()
driver.get('https://html5css.ru/howto/howto_js_rangeslider.php')

# Находим элемент ползунка (замените xpath на реальный xpath элемента)
slider = driver.find_element(By.XPATH, value='//*[@id="id2"]')

# Создаем объект ActionChains
action = ActionChains(driver)

# Пауза для наблюдения
time.sleep(2)

# Двигаем ползунок на -50 пикселей по оси x
action.click_and_hold(slider).move_by_offset(-50, 0).release().perform()
time.sleep(2)  # Пауза после перемещения

# Двигаем ползунок еще на -500 пикселей по оси x
action.click_and_hold(slider).move_by_offset(-500, 0).release().perform()

time.sleep(5) # Чтобы можно было увидеть результат

driver.quit()
