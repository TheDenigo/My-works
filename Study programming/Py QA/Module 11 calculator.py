def calculator():
    try:
        user_input = input("Введите выражение (число1, арифметический знак, число2): ")

        parts = user_input.split()
        
        if len(parts) != 3:
            print("Ошибка: Пожалуйста, введите выражение в формате 'число оператор число'.")
            return

        first_num = float(parts[0])
        operator = parts[1]
        second_num = float(parts[2])

        if operator == '+':
            result = first_num + second_num
            print(f"Результат: {first_num} + {second_num} = {result}")
        elif operator == '-':
            result = first_num - second_num
            print(f"Результат: {first_num} - {second_num} = {result}")
        elif operator == '*':
            result = first_num * second_num
            print(f"Результат: {first_num} * {second_num} = {result}")
        elif operator == '/':
            if second_num == 0:
                print("Ошибка: деление на ноль невозможно!")
            else:
                result = first_num / second_num
                print(f"Результат: {first_num} / {second_num} = {result}")
        else:
            print("Ошибка: неверный арифметический знак. Пожалуйста, используйте +, -, * или /.")
    except ValueError:
        print("Ошибка: пожалуйста, введите числовые значения.")

if __name__ == "__main__":
    calculator()