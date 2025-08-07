import os
import sys
from nbtlib import nbt
from nbtlib import Compound, List
from nbtlib.tag import String, Int, Compound

def find_and_remove_item(nbt_file, target_id):
    """Ищет и удаляет элементы с заданным ID в NBT-файле."""
    try:
        try:
           nbt_data = nbt.load(nbt_file)
        except Exception as e:
           print(f"Файл {nbt_file} не удалось загрузить: {e}, пропускаем.")
           return # Пропускаем некорректные файлы


        if not isinstance(nbt_data, Compound):
            print(f"Файл {nbt_file} не имеет Compound корневой тег, пропускаем.")
            return  # Если нет Compound - пропускаем


        def recursive_search(obj, path=[]):
            """Рекурсивно ищет в NBT-структуре."""
            if isinstance(obj, Compound):
                for key, value in obj.items():
                    if key == "id" and value == target_id:
                        print(f"Удаление {target_id} в {'.'.join(path + [key])} : {value} ")
                        obj.pop(key)
                        return  # Удаляем элемент

                    if isinstance(value, (Compound, List)):
                        recursive_search(value, path + [key])

            if isinstance(obj, List):
                for index, element in enumerate(obj):
                    if isinstance(element, Compound):
                        recursive_search(element, path + [str(index)])

        recursive_search(nbt_data)

        nbt_data.save(nbt_file)  # Сохраняем изменения
        print(f"Изменения сохранены в {nbt_file}")
    except Exception as e:
        print(f"Ошибка при обработке {nbt_file}: {e}")

def process_world_folder(world_folder, target_id):
    """Обрабатывает все NBT-файлы в папке мира Minecraft."""
    print(f"Начало обработки мира {world_folder}")
    for root, _, files in os.walk(world_folder):
        for file in files:
            if file.endswith(".dat") or file.endswith(".mca"):
                full_path = os.path.join(root, file)
                print(f"Проверка {full_path}")
                find_and_remove_item(full_path, target_id)

    print("Обработка мира завершена")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python script.py <папка_мира> <искомый_id>")
        sys.exit(1)

    world_folder = sys.argv[1]
    target_id = sys.argv[2]

    if not os.path.isdir(world_folder):
        print(f"Ошибка: папка '{world_folder}' не найдена.")
        sys.exit(1)

    process_world_folder(world_folder, target_id)