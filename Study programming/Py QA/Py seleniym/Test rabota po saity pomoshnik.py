from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

try:
    # Шаг 1: Авторизация
    print("-----------------------")
    print("Этап авторизации")
    
    # 1. Открываем сайт
    driver.get("https://www.saucedemo.com/")
    
    # 2. Находим поле для ввода имени пользователя
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )
    
    # 3. Вводим имя пользователя
    username_field.send_keys("standard_user")
    
    # 4. Находим поле для ввода пароля
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    
    # 5. Вводим пароль
    password_field.send_keys("secret_sauce")
    
    # 6. Нажимаем Enter для авторизации
    password_field.send_keys(Keys.RETURN)
    
    # 7. Ожидаем, что перешли на страницу с товарами (можно ожидать появления любого характерного элемента)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
    )
    
    print("Успешная авторизация!")

    # Шаг 2: Получение списка товаров и выбор товара
    print("-----------------------")
    print("Этап выбора товара")
    
    def get_product_list():
        """Получает список названий всех товаров на странице"""
        product_names = []
        inventory_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        for item in inventory_items:
            try:
                name_element = item.find_element(By.CLASS_NAME, "inventory_item_name")
                product_names.append(name_element.text)
            except NoSuchElementException:
                print("Не удалось найти имя товара")
        return product_names


    def scroll_page():
        """Прокручивает страницу вниз и вверх для загрузки всех элементов"""
        # Прокручиваем вниз
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        # Прокручиваем вверх
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)

    def choose_product():
        """Позволяет пользователю выбрать несколько продуктов и добавляет их в корзину"""
        scroll_page()
        products = get_product_list()
        if not products:
            print("Нет товаров на странице.")
            return False
        
        print("Доступные товары:")
        for i, product in enumerate(products):
            print(f"{i + 1}. {product}")
        
        chosen_products = []
        while True:
            try:
                choice = input("Выберите номер товара для добавления в корзину (или 'готово', если закончили): ")
                if choice.lower() == 'готово':
                    break
                choice = int(choice)
                if 1 <= choice <= len(products):
                     if products[choice - 1] not in chosen_products:
                       chosen_products.append(products[choice - 1])
                       print (f"Товар {products[choice - 1]} добавлен")
                     else:
                        print ("Такой товар уже добавлен.")

                else:
                    print("Неверный выбор. Пожалуйста, введите число от 1 до", len(products))
            except ValueError:
                print("Неверный формат ввода. Введите номер товара или 'готово'.")
            
        if not chosen_products:
            print("Вы не выбрали ни одного товара.")
            return False
            
        # Добавляем выбранные товары в корзину
        inventory_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        for product_name in chosen_products:
              for item in inventory_items:
                  try:
                        name_element = item.find_element(By.CLASS_NAME, "inventory_item_name")
                        if name_element.text == product_name:
                            add_to_cart_button = item.find_element(By.XPATH, ".//button[text()='Add to cart']")
                            add_to_cart_button.click()
                            print(f'Товар "{product_name}" добавлен в корзину')
                            break;
                  except NoSuchElementException:
                        print(f"Не удалось найти товар или кнопку добавления в корзину для {product_name}")
        
        return True

    if choose_product() == False:
        driver.quit()
        exit()
    

    # Шаг 3: Проверка и переход в корзину
    print("-----------------------")
    print("Этап перехода в корзину")
    
    def go_to_cart():
        """Переходит в корзину и проверяет наличие товаров"""
        try:
                cart_button = WebDriverWait(driver,10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
                )
                cart_button.click()
                print("Переход в корзину")

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
                )
                return True
        except NoSuchElementException:
                print("Ошибка: Не найдена кнопка корзины.")
                return False
        except TimeoutException:
            print("Ошибка: Истекло время ожидания перехода в корзину")
            return False
        except Exception as e:
            print("Неизвестная ошибка при переходе в корзину", e)
            return False

    if go_to_cart() == False:
        driver.quit()
        exit()
    
    # Шаг 4: Просмотр товаров в корзине и их подтверждение
    print("-----------------------")
    print("Этап просмотра корзины")
    
    def review_cart():
            """Просматривает товары в корзине и дает возможность их удалить"""
            
            cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
            
            if not cart_items:
               print ("В корзине нет товаров")
               return False
            
            print("Ваши товары в корзине:")
            
            
            items_in_cart = []
            for i, item in enumerate(cart_items):
                try:
                    name_element = item.find_element(By.CLASS_NAME, "inventory_item_name")
                    items_in_cart.append(name_element.text)
                    print(f"{i + 1}. {name_element.text}")
                except NoSuchElementException:
                   print("Не удалось найти наименование товара")
            
            while True:
                 action = input("Хотите удалить товары (да/нет) или перейти к оплате (оплата)? ")
                 if action.lower() == 'да':
                    while True:
                        try:
                            
                            remove_choice = int(input("Введите номер товара, который нужно удалить, или 0, если закончили: "))
                            if remove_choice == 0:
                                break
                            if 1 <= remove_choice <= len(items_in_cart):
                                item_to_remove = items_in_cart[remove_choice-1]
                                cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
                                for item in cart_items:
                                    try:
                                        name_element = item.find_element(By.CLASS_NAME, "inventory_item_name")
                                        if name_element.text == item_to_remove:
                                            remove_button = item.find_element(By.XPATH, ".//button[text()='Remove']")
                                            remove_button.click()
                                            print(f"Товар {item_to_remove} был удален")
                                            items_in_cart.remove(item_to_remove)
                                            break
                                    except NoSuchElementException:
                                        print("Не удалось найти кнопку для удаления")
                                
                            else:
                                print("Неверный номер товара. Пожалуйста, выберите один из списка, либо 0")
                        except ValueError:
                            print ("Неверный формат ввода")
                    
                    if not items_in_cart:
                      print("В корзине нет товаров")
                      return False
                    
                    print ("Список товаров после изменения")
                    for i, item in enumerate(items_in_cart):
                      print(f"{i+1}. {item}")
                    
                    break;

                 elif action.lower() == "оплата":
                    return True
                 elif action.lower() == "нет":
                     return False
                 else:
                    print("Неверная команда")

    if review_cart() == False:
        driver.quit()
        exit()
    
    # Шаг 5: Ввод данных и подтверждение заказа
    print("-----------------------")
    print("Этап оформления заказа")
    
    def fill_checkout_form():
        """Заполняет форму заказа и переходит на следующий этап"""
        try:
            checkout_button = WebDriverWait(driver,10).until(
                EC.element_to_be_clickable((By.ID, "checkout"))
            )
            checkout_button.click()
            print("Переход к форме оформления заказа.")
            
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "first-name"))
            )


            first_name = input("Введите ваше имя: ")
            last_name = input("Введите вашу фамилию: ")
            postal_code = input("Введите ваш почтовый индекс: ")
            
            
            first_name_field = driver.find_element(By.ID, "first-name")
            first_name_field.send_keys(first_name)
            
            last_name_field = driver.find_element(By.ID, "last-name")
            last_name_field.send_keys(last_name)
            
            postal_code_field = driver.find_element(By.ID, "postal-code")
            postal_code_field.send_keys(postal_code)
            
            continue_button = driver.find_element(By.ID, "continue")
            continue_button.click()
            
            print("Переход к обзору заказа.")
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_info"))
            )
            return True

        except NoSuchElementException:
            print("Ошибка: Не удалось найти поле ввода или кнопку далее.")
            return False
        except TimeoutException:
            print("Ошибка: Истекло время ожидания при заполнении формы")
            return False
        except Exception as e:
            print("Неизвестная ошибка при заполнении формы", e)
            return False

    if fill_checkout_form() == False:
        driver.quit()
        exit()
    
    # Шаг 6: Подтверждение заказа и финиш
    print("-----------------------")
    print("Этап подтверждения и завершения заказа")
    
    def confirm_order():
            try:
                # Прокручиваем страницу вниз, потом вверх для загрузки элементов
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(2)

                items_in_overview = driver.find_elements(By.CLASS_NAME, "cart_item")

                if not items_in_overview:
                   print("Обзор заказа не содержит товаров")
                   return False
                
                print("Товары к заказу:")
                for item in items_in_overview:
                    try:
                        name_element = item.find_element(By.CLASS_NAME, "inventory_item_name")
                        print (name_element.text)
                    except NoSuchElementException:
                        print ("Не удалось найти имя товара в обзоре")

                total_price_element = driver.find_element(By.CLASS_NAME, "summary_total_label")
                print("Итоговая сумма заказа:", total_price_element.text)


                try:
                     shipping_info_element = driver.find_element(By.CLASS_NAME, "summary_info_label.summary_delivery_label")
                     print("Информация о доставке:", shipping_info_element.text)
                except NoSuchElementException:
                  print("Информация о доставке не найдена.")
                
                try:
                   payment_info_element = driver.find_element(By.CLASS_NAME, "summary_info_label.summary_payment_label")
                   print("Способ оплаты:", payment_info_element.text)
                except NoSuchElementException:
                  print("Информация о способе оплаты не найдена.")
                
                
                confirm = input("Подтвердить заказ? (да/нет): ")
                if confirm.lower() == "да":
                    finish_button = driver.find_element(By.ID, "finish")
                    finish_button.click()
                    print("Заказ подтвержден.")
                    WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
                    )
                    print("Спасибо за покупку")
                    return True
                else:
                    print("Заказ отменен")
                    return False

            except NoSuchElementException:
                print("Ошибка не найден элемент на странице обзора")
                return False
            except TimeoutException:
                print("Ошибка: Истекло время ожидания при подтверждении заказа")
                return False
            except Exception as e:
                print("Неизвестная ошибка при подтверждении заказа", e)
                return False

    if confirm_order() == False:
        driver.quit()
        exit()

except NoSuchElementException as e:
    print ("Проблема с поиском элемента", e)
except TimeoutException as e:
    print ("Истекло время ожидания", e)
except Exception as e:
    print("Произошла непредвиденная ошибка", e)
finally:
    driver.quit()