import os

def sort_lines(input_file, output_file):
    # Проверка наличия входного файла
    if not os.path.exists(input_file):
        print(f"Файл '{input_file}' не найден. Создание нового файла.")
        with open(input_file, 'w') as file:
            print("Введите строки для добавления в файл (или 'exit' для завершения ввода):")
            while True:
                line = input()
                if line.lower() == 'exit':
                    break
                file.write(line + '\n')
    
    # Чтение строк из файла
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    # Проверка наличия записей в файле
    if not lines:
        print(f"Файл '{input_file}' пуст. Пожалуйста, введите данные (для завершения ввода введите 'exit'):")
        while True:
            line = input()
            if line.lower() == 'exit':
                break
            # Запись введенных пользователем строк в файл
            with open(input_file, 'a') as file:  # Используем режим 'a' для добавления
                file.write(line + '\n')
        # Считываем строки снова
        with open(input_file, 'r') as file:
            lines = file.readlines()

    # Сортировка строк
    lines = [line.strip() for line in lines]
    sorted_lines = sorted(lines)

    # Запись отсортированных строк в выходной файл
    try:
        with open(output_file, 'w') as file:
            for line in sorted_lines:
                file.write(line + '\n')
        print(f"\nОтсортированные строки записаны в файл '{output_file}':")
        for line in sorted_lines:
            print(line)
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")

def main():
    input_file = 'input.txt'  # Файл для ввода
    output_file = 'output.txt'  # Файл для вывода
    print(f"Работа с файлами:\nВходной файл: {os.path.abspath(input_file)}\nВыходной файл: {os.path.abspath(output_file)}\n")
    sort_lines(input_file, output_file)

if __name__ == '__main__':
    main()