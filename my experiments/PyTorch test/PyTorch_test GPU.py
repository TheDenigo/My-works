import torch

# Проверяем доступность GPU
if torch.cuda.is_available():
    device = torch.device('cuda')
    print("GPU is available. Using device:", device)
else:
    device = torch.device('cpu')
    print("GPU is not available. Using device:", device)

# Создаем тензор на GPU
x = torch.randn(3, 4, device=device)

# Выполняем простые операции (на GPU)
y = x + 2
z = x * y

# Выводим результаты (тензоры копируются на CPU для вывода)
print("x:\n", x.cpu())
print("y:\n", y.cpu())
print("z:\n", z.cpu())