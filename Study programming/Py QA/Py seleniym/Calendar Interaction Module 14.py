from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime
import time

# Инициализация драйвера (пример для Chrome)
driver = webdriver.Chrome()
driver.get('https://demoqa.com/date-picker')

# Получаем элемент input поля календаря
date_input = driver.find_element(By.XPATH, value='//*[@id="datePickerMonthYearInput"]')

# Очищаем поле ввода
date_input.send_keys(Keys.CONTROL + 'a')
date_input.send_keys(Keys.DELETE)
time.sleep(2)

# Получаем текущую дату
current_date = datetime.datetime.now()
# Форматируем дату в нужный формат (месяц, день, год)
current_date = current_date.strftime("%m/%d/%Y")

# Вставляем отформатированную дату в поле
date_input.send_keys(current_date)

time.sleep(5) # Чтобы можно было увидеть результат

driver.quit()
