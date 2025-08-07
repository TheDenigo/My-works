# module_4_1.py

from fake_math import divide as fake_divide
from true_math import divide as true_divide

result1 = fake_divide(69, 3)  # обычное деление
result2 = fake_divide(3, 0)    # деление на 0 (ошибка)
result3 = true_divide(49, 7)   # обычное деление
result4 = true_divide(15, 0)   # деление на 0 (бесконечность)

print(result1)
print(result2)
print(result3)
print(result4)