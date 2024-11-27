import shutil
import asyncio
from pathlib import Path
import logging
from colorama import Fore, Style
import textwrap

# Налаштування логування
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(message)s")

# Асинхронна функція для копіювання файлів


async def copy_file(file_path, dest_folder):
    try:
        # Отримання розширення файлу
        file_extension = file_path.suffix.lstrip(".").lower()
        if not file_extension:
            file_extension = "unknown"

        # Створення папки для розширення
        dest_path = dest_folder / file_extension
        dest_path.mkdir(parents=True, exist_ok=True)

        # Копіювання файлу
        await asyncio.to_thread(shutil.copy, file_path, dest_path)
       # Форматування довгих рядків
        formatted_message = textwrap.fill(
            f"Файл {file_path.name} скопійовано в {dest_path}",
            width=120
        )
        print(Fore.GREEN + formatted_message + Style.RESET_ALL)
    except Exception as e:
        logging.error(f"Помилка копіювання файлу {file_path}: {e}")
        print(
            Fore.RED + f"Помилка копіювання файлу {file_path}: {e}" + Style.RESET_ALL)

# Асинхронна функція для читання папки


async def read_folder(source_folder, dest_folder):
    try:
        tasks = []
        # Проходимося по всіх файлах та папках
        for item in source_folder.iterdir():
            if item.is_file():
                tasks.append(copy_file(item, dest_folder))
            elif item.is_dir():
                tasks.append(read_folder(item, dest_folder))
        # Виконуємо завдання асинхронно
        await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"Помилка читання папки {source_folder}: {e}")
        print(
            Fore.RED + f"Помилка читання папки {source_folder}: {e}" + Style.RESET_ALL)

# Головна функція


def main():
    print(Fore.BLUE + "Вкажіть шлях до папки для сортування" + Style.RESET_ALL)

    # Запит на шлях до вихідної папки
    source_folder_path = input(
        Fore.YELLOW + "Введіть шлях до вихідної папки: " + Style.RESET_ALL).strip()

    # Запит на шлях до цільової папки
    sorted_folder_path = input(
        Fore.YELLOW + "Введіть шлях до цільової папки: " + Style.RESET_ALL).strip()

    # Перетворення шляхів у Path
    source_folder = Path(source_folder_path)
    sorted_folder = Path(sorted_folder_path)

    # Перевірка наявності вихідної папки
    if not source_folder.is_dir():
        print(
            Fore.RED + "Помилка: Вихідна папка не існує або це не папка." + Style.RESET_ALL)
        return

    print(Fore.BLUE + "Розпочинається сортування файлів..." + Style.RESET_ALL)
    asyncio.run(read_folder(source_folder, sorted_folder))
    print(Fore.BLUE + "Сортування завершено." + Style.RESET_ALL)


if __name__ == "__main__":
    main()
