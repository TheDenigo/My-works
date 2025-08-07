
my_string = input("Введите произвольный текст: ")

print(f"Количество символов в введенном тексте: {len(my_string)}")

print(f"Строка в верхнем регистре: {my_string.upper()}")

print(f"Строка в нижнем регистре: {my_string.lower()}")

my_string_no_spaces = my_string.replace(" ", "")
print(f"Строка без пробелов: {my_string_no_spaces}")

print(f"Первый символ строки: {my_string[0:1]}")

print(f"Последний символ строки: {my_string[-1:]})")