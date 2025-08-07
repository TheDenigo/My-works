from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализируем веб-драйвер
driver = webdriver.Edge()

# Открываем нужный сайт
driver.get("https://demoqa.com/checkbox")

# 1. Кнопка "Expand all" (раскрыть все)
main_toggle_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Expand all"]'))
)
main_toggle_button.click()
print(f"Клик на кнопку раскрытия дерева: {main_toggle_button}")

# 2. Чекбокс "Home"
home_check_box = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//label[@for="tree-node-home"]/span[@class="rct-checkbox"]'))
)
home_check_box.click()
print(f"Клик на чекбокс Home: {home_check_box}")

# 3. Проверяем, выбран ли чекбокс (лучше проверять состояние input)
home_check_box_input = driver.find_element(By.XPATH, '//input[@id="tree-node-home"]')
is_selected = home_check_box_input.is_selected()
print(f"Чекбокс Home выбран: {is_selected}")  # Вывод состояния чекбокса

# Закрываем драйвер
driver.quit()

#кнопка +
# /html/body/div[2]/div/div/div/div[2]/div[2]/div/div/button[1]
# //*[@id="tree-node"]/div/button[1]
# тогл
# //*[@id="tree-node"]/ol/li/span/button
# /html/body/div[2]/div/div/div/div[2]/div[2]/div/ol/li/span/button