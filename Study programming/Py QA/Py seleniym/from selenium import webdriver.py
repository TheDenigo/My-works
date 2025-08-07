from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://demoqa.com/checkbox")

try:
    # Найти и щелкнуть на чекбокс
    checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".rct-checkbox > div > svg"))
    )
    checkbox.click()

    # Найти и щелкнуть на тумблер
    toggle = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div > button"))
    )
    toggle.click()

except Exception as e:
    print("Ошибка:", str(e))
finally:
    driver.quit()