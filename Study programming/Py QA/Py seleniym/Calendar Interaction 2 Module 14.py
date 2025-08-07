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
# Добавляем 10 дней
future_date = current_date + datetime.timedelta(days=10)
# Форматируем будущую дату в нужный формат (месяц/день/год)
future_date_formatted = future_date.strftime("%m/%d/%Y")

# Вставляем отформатированную дату в поле
date_input.send_keys(future_date_formatted)

# Выводим сообщение о выполнении
print(f"Дата, на 10 дней позже текущей ({future_date_formatted}), успешно введена в поле.")

time.sleep(8) # Чтобы можно было увидеть результат

driver.quit()