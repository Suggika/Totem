import os
from config import *

def search_local_files():
    Title("Поиск по БД")
    try:
        print(colorize(Database))
        path = input(get_prompt("Введите путь к папке с файлами"))
        if not os.path.isdir(path):
            log_message(ERROR, "Указанный путь не является директорией или не существует.")
            return
        
        query = input(get_prompt("Введите информацию для поиска"))
        log_message(INFO, f"Идет поиск по запросу: {query}")
        log_message(WAIT, "Идет поиск в локальных файлах...")

        found_count = 0
        for root, _, files in os.walk(path):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            if query.lower() in line.lower():
                                found_count += 1
                                print(f"[+] Найдено в файле: {file_path} | Строка {line_num}: {line.strip()}")
                except Exception:
                    continue
        
        if found_count == 0:
            log_message(INFO, "По вашему запросу ничего не найдено.")
        else:
            log_message(INFO, f"Поиск завершен. Всего найдено совпадений: {found_count}")

    except Exception as e:
        Error(e)
