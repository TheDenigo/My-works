from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
import time
import getpass

def analyze_website(driver: WebDriver, url: str):
    """Анализирует веб-сайт и возвращает отчет о его функциональности."""

    try:
        driver.get(url)
        print(f"Анализ сайта: {url}")

        links = get_all_links(driver)
        buttons = get_all_buttons(driver)
        forms = get_all_forms(driver)

        link_results = check_links(driver, links)
        form_analysis_results = analyze_forms(driver, forms) # Анализируем формы

        report = {
            "links": link_results,
            "buttons": buttons,
            "forms": form_analysis_results,
        }

        return report

    except Exception as e:
        print(f"Произошла ошибка при анализе сайта: {e}")
        return None

def get_all_links(driver: WebDriver):
    """Возвращает список всех ссылок на странице."""
    links = driver.find_elements(By.TAG_NAME, "a")
    return [link.get_attribute("href") for link in links if link.get_attribute("href")] # Фильтруем пустые ссылки

def check_links(driver: WebDriver, links):
    """Проверяет, доступны ли ссылки."""
    results = {}
    for link in links:
        try:
            driver.get(link)
            results[link] = driver.current_url == link
            driver.back()
        except Exception as e:
            results[link] = False
            print(f"Ошибка при проверке ссылки {link}: {e}")
    return results

def get_all_buttons(driver: WebDriver):
    """Возвращает список всех кнопок на странице."""
    buttons = driver.find_elements(By.TAG_NAME, "button")
    return [button.text for button in buttons]

def get_all_forms(driver: WebDriver):
    """Возвращает список всех форм на странице."""
    forms = driver.find_elements(By.TAG_NAME, "form")
    return forms

def analyze_forms(driver: WebDriver, forms):
    """Анализирует формы на странице, включая авторизацию."""
    results = {}
    print(f"Найдено форм: {len(forms)}") # Лог
    for form in forms:
        try:
            form_name = form.get_attribute("name") or "Unnamed Form"
            print(f"Анализируем форму: {form_name}") # Лог
            results[form_name] = analyze_form(driver, form)
        except Exception as e:
            print(f"Ошибка при анализе формы {form_name}: {e}") # Лог
            results[form_name] = f"Ошибка при анализе: {e}"
    return results

def analyze_form(driver: WebDriver, form):
    """Анализирует одну форму, определяет, является ли она формой авторизации, и обрабатывает ее."""
    try:
        inputs = form.find_elements(By.TAG_NAME, "input")
        input_types = [input.get_attribute("type") for input in inputs]
        print(f"Типы полей формы: {input_types}") # Лог

        if "password" in input_types and ("email" in input_types or "text" in input_types):
            print("Обнаружена форма авторизации!")
            return handle_login_form(driver, form)
        else:
            print("Обнаружена обычная форма.")
            return check_normal_form(driver, form)
    except Exception as e:
        print(f"Ошибка при анализе типа формы: {e}")
        return f"Ошибка при анализе типа: {e}"


def handle_login_form(driver: WebDriver, form):
    """Обрабатывает форму авторизации."""
    try:
        print("Начинаем обработку формы авторизации...") # Лог

        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")

        # Логируем атрибуты формы
        print(f"Атрибуты формы: {form.get_attribute('outerHTML')}")

        username_field = None
        password_field = None

        try:
            username_field = form.find_element(By.ID, "user-name")
            print("Найдено поле username по ID: user-name") # Лог
        except:
            print("Не удалось найти поле username по ID: user-name")

        try:
            password_field = form.find_element(By.ID, "password")
            print("Найдено поле password по ID: password") # Лог
        except:
            print("Не удалось найти поле password по ID: password")

        # Дополнительные попытки поиска поля username
        if not username_field:
            print("Не удалось найти поле username/email.") # Лог

            try:
                username_field = form.find_element(By.CSS_SELECTOR, "[data-test='username']")
                print("Найдено поле username по CSS селектору [data-test='username']")
            except:
                print("Не удалось найти поле username по CSS селектору [data-test='username']")

        if not password_field:
            print("Не удалось найти поле password.") # Лог

            # Дополнительные попытки поиска поля password
            try:
                password_field = form.find_element(By.CSS_SELECTOR, "[data-test='password']")
                print("Найдено поле password по CSS селектору [data-test='password']")
            except:
                print("Не удалось найти поле password по CSS селектору [data-test='password']")

        if not username_field:
            print("Все еще не удалось найти поле username/email.")
            return "Не удалось найти поле username/email."
        if not password_field:
            print("Все еще не удалось найти поле password.")
            return "Не удалось найти поле password."

        username_field.send_keys(username)
        password_field.send_keys(password)

        # Ищем кнопку submit (предполагаем, что она есть)
        submit_button = form.find_element(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
        submit_button.click()

        time.sleep(5)

        if "ошибка" in driver.page_source.lower() or "failed" in driver.page_source.lower(): # Проверяем наличие слов "ошибка" или "failed" на странице
            return "Авторизация не удалась."
        else:
            return "Авторизация прошла успешно."

    except Exception as e:
        print(f"Ошибка при обработке формы авторизации: {e}")
        return f"Ошибка при авторизации: {e}"

def check_normal_form(driver: WebDriver, form):
  """Проверяет обычную форму (простой пример)."""
  try:
    inputs = form.find_elements(By.TAG_NAME, "input")
    text_inputs = [i for i in inputs if i.get_attribute('type') == 'text']
    if text_inputs:
      text_inputs[0].send_keys("test")

    # Отправляем форму (если есть кнопка submit)
    submit_buttons = form.find_elements(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
    if submit_buttons:
      submit_buttons[0].click()
      time.sleep(2)
      driver.back()
      return "Форма отправлена."
    else:
      return "Нет кнопки Submit."

  except Exception as e:
    print(f"Ошибка при проверке обычной формы: {e}")
    return f"Ошибка: {e}"

if __name__ == "__main__":
    url = input("Введите URL сайта для анализа: ")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)


    report = analyze_website(driver, url)

    if report:
        print("Отчет об анализе:")
        print("Ссылки:")
        for link, result in report["links"].items():
            print(f"  {link}: {'OK' if result else 'Ошибка'}")

        print("\nКнопки:")
        for button in report["buttons"]:
            print(f"  {button}")

        print("\nФормы:")
        for form_name, result in report["forms"].items():
            print(f"  {form_name}: {result}")
    else:
        print("Анализ не удался.")


    driver.quit()
