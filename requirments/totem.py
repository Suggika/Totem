r""" 
ИСХОДНИКИ ДЛЯ НЕКОТОРЫХ ФУНКЦИЙ БЫЛИ ВЗЯТЫ ИЗ СОФТА

______         _   _____ _                 
| ___ \       | | |_   _(_)                
| |_/ /___  __| |   | |  _  __ _  ___ _ __ 
|    // _ \/ _` |   | | | |/ _` |/ _ \ '__|
| |\ \  __/ (_| |   | | | | (_| |  __/ |   
\_| \_\___|\__,_|   \_/ |_|\__, |\___|_|   
                            __/ |          
                           |___/            """



import os
import webbrowser
import time
import sys
import re
import requests 

from config import *
from phone_number_lookup import lookup_phone
from ip_lookup import lookup_ip
from email_lookup import lookup_email
from local_search import search_local_files
from leak_osint import search_leak_osint

try:
    from username_tracker import track_username
except ImportError:
    def track_username():
        log_message(ERROR, "Модуль 'username_tracker.py' не найден.")
        
try:
    from website_lookup import lookup_website
except ImportError:
    def lookup_website():
        log_message(ERROR, "Модуль 'website_lookup.py' не найден.")

PROFILE_FILE = "profile.txt"
VK_TOKEN = "0af157510af157510af15751aa0a89e69600af10af157516a0bc15996e74fe2b440998c" 

# --- НОВЫЕ ФУНКЦИИ ДЛЯ ПОИСКА VK ---

def perform_vk_search(query):
    """Выполняет запрос к API VK."""
    url = "https://api.vk.com/method/users.get"
    params = {
        'access_token': VK_TOKEN,
        'v': '5.131',
        'user_ids': query,
        'fields': 'first_name,last_name,status,sex,city,country,photo_50,photo_100,photo_200,bdate,home_town,about,interests,books,movies,music,quotes,relation,mobile_phone,home_phone,site,education,occupation,last_seen,followers_count,is_friend'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на HTTP ошибки
        data = response.json()
        if 'response' in data and len(data['response']) > 0:
            return data['response'][0]
    except requests.exceptions.RequestException as e:
        log_message(ERROR, f"Ошибка сети при запросе к VK API: {e}")
    except Exception as e:
        log_message(ERROR, f"Неожиданная ошибка при работе с VK API: {e}")
    return None

def format_vk_results(user):
    """Форматирует результаты поиска VK для вывода в консоль."""
    if not user:
        return colorize("❌ Пользователь не найден.", ANSI_COLORS.get("RED"))

    result_lines = [
        "────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────"
    ]

    def add_line(key, value):
        if value:
            result_lines.append(f" {ADD} {key.ljust(22)}: {value}")

    add_line("ID", user.get('id'))
    add_line("Имя", user.get('first_name'))
    add_line("Фамилия", user.get('last_name'))

    sex = user.get('sex')
    sex_str = "Мужской" if sex == 2 else "Женский" if sex == 1 else "Не указан"
    add_line("Пол", sex_str)

    add_line("Дата рождения", user.get('bdate'))
    
    city = user.get('city', {}).get('title')
    country = user.get('country', {}).get('title')
    add_line("Город", city)
    add_line("Страна", country)
    add_line("Родной город", user.get('home_town'))
    
    add_line("Статус", user.get('status'))
    
    relation_map = {
        1: "Не женат/не замужем", 2: "Есть друг/подруга", 3: "Помолвлен(а)",
        4: "Женат/замужем", 5: "Всё сложно", 6: "В активном поиске",
        7: "Влюблен(а)", 0: "Не указано"
    }
    add_line("Семейное положение", relation_map.get(user.get('relation')))
    
    add_line("Телефон", user.get('mobile_phone'))
    add_line("Сайт", user.get('site'))
    
    occupation = user.get('occupation', {})
    if occupation:
        occ_type = occupation.get('type', '').capitalize()
        occ_name = occupation.get('name', '')
        add_line("Деятельность", f"{occ_type}: {occ_name}")

    add_line("Подписчики", user.get('followers_count'))
    
    last_seen_info = user.get('last_seen')
    if last_seen_info:
        last_seen_ts = last_seen_info.get('time')
        last_seen_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_seen_ts))
        add_line("Последний онлайн", last_seen_str)

    add_line("О себе", user.get('about'))
    add_line("Интересы", user.get('interests'))
    add_line("Музыка", user.get('music'))
    add_line("Фильмы", user.get('movies'))
    add_line("Книги", user.get('books'))
    add_line("Цитаты", user.get('quotes'))

    add_line("Фото (50px)", user.get('photo_50'))
    add_line("Фото (100px)", user.get('photo_100'))
    add_line("Фото (200px)", user.get('photo_200'))

    result_lines.append(
        "────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────"
    )
    return "\n".join(result_lines)

def lookup_vk():
    """Основная функция для поиска по VK."""
    Title("VK User Search")
    try:
        print(colorize(VK))
        query = input(get_prompt("Введите ID пользователя:"))
        if not query:
            log_message(ERROR, "Запрос не может быть пустым.")
            return

        log_message(WAIT, f"Ищу информацию о пользователе VK: {query}...")
        user_data = perform_vk_search(query)
        result = format_vk_results(user_data)
        Slow(result)
    except Exception as e:
        Error(e)




def load_profile():
    if not os.path.exists(PROFILE_FILE):
        return "guest", "default"
    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            parts = f.read().strip().split("|")
            if len(parts) >= 3:
                nick = parts[0]
                theme_name = parts[2]
                set_theme(theme_name)
                return nick, theme_name
    except Exception as e:
        print(f"[x] Не удалось прочитать профиль: {e}")
    return "guest", "default"

banner = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠖⡿⠛⠑⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡠⠒⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢾⠒⡤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⢄⣀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣏⣺⣼⣛⣤⣾⠟⠀⠀⠀⠀⠀⢀⡴⠒⢩⢧⣼⣿⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⡿⣶⣻⣘⡗⣤⣄⣀⠀⠀⠀⠀⢀⡤⢾⣍⠙⣦⡌⣳⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢘⣿⣿⣿⣿⣧⡀⠀⠀⣀⡤⠒⣫⣶⣼⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⢿⣿⣿⣿⣷⣌⠬⣑⣄⠀⠀⣾⣤⡀⣹⣦⣿⣷⣏⠀⠀⠀⠀⠀
⠀⠀⠀⣠⠖⠀⠒⢄⣞⣻⣿⣿⣿⣿⣷⣀⡜⠁⣰⣏⣻⣿⡿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢿⣿⣿⡻⢷⣮⣕⣦⣼⣿⣿⣿⣿⣿⣿⢿⡠⠤⢄⡀⠀
⠀⠀⠰⣿⢠⡄⠀⣠⡌⠹⢽⣿⡽⣾⣽⣧⣦⣾⢃⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣟⣳⣾⣿⣿⣿⣿⣿⣿⡿⠿⠛⠋⠀⠀⠄⣿⡄
⠀⠀⠀⠙⣿⣿⣰⡇⠀⣤⢨⣿⣿⣿⣿⣿⣿⣼⡟⣯⡟⠁⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠙⣿⣯⣻⢿⣿⣿⣿⢟⠙⠶⢦⣀⢣⣴⣸⣿⠟⠁
⠀⠀⠀⣀⣿⣿⣿⣿⣾⣷⣿⣿⣿⣿⣿⣿⢻⣱⣾⠟⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠘⢿⣯⣿⣽⣿⣿⣖⣧⣀⣾⣧⣿⣿⣿⣇⠀⠀
⠀⢠⣿⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⢿⣹⣬⣷⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⣿⠅⠈⠀⠁⠀⢽⣿⣿⣿⠀⠁⠈⠀⠁⣿⡿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣷⠀
⠀⢸⣿⣀⠀⠈⣻⢿⣿⣿⣿⡿⣿⣾⣯⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⢽⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈   ⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠻⡄
⠀⣠⡿⣿⢱⡏⠈⠁⣹⣿⢿⣿⣿⡿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⢽⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⡿⠟⠉⠀⢀⢲⣿
⠀⡟⠀⡿⢻⣷⣾⣷⣿⣿⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀    ⢽⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡟⠫⠵⢦⣀⣳⣶⣿⣿⠏
⢰⠇⠘⢇⣿⣿⣿⣿⣯⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀    ⠀⢽⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⣷⣣⣾⣿⣿⣿⣿⠏⠀
⢸⠀⠀⣬⡟⠛⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀     ⠀⣹⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⣼⠟⢓⣾⡏⠀⠀
⢸⠂⢀⡾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀       ⢺⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⣼⠃⡎⣼⠟⠀⠀⠀
⠻⠶⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀       ⠈⠙⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢾⣁⣼⡟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀       ⣿⣈⡽⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀       ⠀⢈⣉⠀⠀⠀⠀⠀⠀⠀⠀



 _________________       _____   _________________      ______        ______  _______   
/                 \ ____|\    \ /                 \ ___|\     \      |      \/       \  
\______     ______//     /\    \\______     ______/|     \     \    /          /\     \ 
   \( /    /  )/  /     /  \    \  \( /    /  )/   |     ,_____/|  /     /\   / /\     |
    ' |   |   '  |     |    |    |  ' |   |   '    |     \--'\_|/ /     /\ \_/ / /    /|
      |   |      |     |    |    |    |   |        |     /___/|  |     |  \|_|/ /    / |
     /   //      |\     \  /    /|   /   //        |     \____|\ |     |       |    |  |
    /___//       | \_____\/____/ |  /___//         |____ '     /||\____\       |____|  /
   |`   |         \ |    ||    | / |`   |          |    /_____/ || |    |      |    | / 
   |____|          \|____||____|/  |____|          |____|     | / \|____|      |____|/  
     \(               \(    )/       \(              \( |_____|/     \(          )/     
      '                '    '         '               '    )/         '          '      
                                                           '                            
"""

banner2 = r"""
        __,---.
       /__|o\  )    {...} Powered by Totem Launcher
        `-\ / /     
          ,) (,     >_ Version 1.6
         //   \\    
        {(     )}   Made by @suggika
  =======""===""==================================
          |||||     Full Version --> @TotemKmBot
           |||
            |
"""

banner3 = r"""
╭─────────────────────────────────────────╮
│   _____ _________    ____  ________  __ │
│  / ___// ____/   |  / __ \/ ____/ / / / │
│  \__ \/ __/ / /| | / /_/ / /   / /_/ /  │
│ ___/ / /___/ ___ |/ _, _/ /___/ __  /   │
│/____/_____/_/  |_/_/ |_|\____/_/ /_/    │
├─────────────────────────────────────────┤
│ 01 > Phone        05 > Website Info     │
│ 02 > Username     06 > Database         │
│ 03 > IP           07 > Leak Osint       │
│ 04 > Email        08 > VK               │
╰─────────────────────────────────────────╯
"""

banner4 = r"""
╭───────────────────────────────────────╮
│        _____  ___  ___  __  __        │
│       /__   \/___\/___\/ / / _\       │
│        / /\//  ///  // /  \ \         │
│       / / / \_// \_// /____\ \        │
│       \/  \___/\___/\____/\__/        │
├───────────────────────────────────────┤
│ 09 > Stealer                          │
│ 10 > RAT                              │
│ 11 > IP Stealer - Telegram Call       │
│ 12 > Discord Self Bot                 │
╰───────────────────────────────────────╯
"""

def combine_banners_side_by_side(left_text, right_text, separator="   "):
    left_lines = left_text.strip('\n').split('\n')
    right_lines = right_text.strip('\n').split('\n')
    
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    
    max_left_width = max(len(ansi_escape.sub('', line)) for line in left_lines) if left_lines else 0
    num_lines = max(len(left_lines), len(right_lines))
    
    combined_lines = []
    for i in range(num_lines):
        left_line = left_lines[i] if i < len(left_lines) else ""
        right_line = right_lines[i] if i < len(right_lines) else ""
        
        plain_left_line_len = len(ansi_escape.sub('', left_line))
        padding = " " * (max_left_width - plain_left_line_len)
        
        combined_lines.append(f"{left_line}{padding}{separator}{right_line}")
        
    return "\n".join(combined_lines)

def print_centered(text):
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80
    
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    for line in text.split('\n'):
        plain_line = ansi_escape.sub('', line)
        padding = (terminal_width - len(plain_line)) // 2
        print(' ' * max(0, padding) + line)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    
    user_nick, theme_name = load_profile()
    os_name = os.name if os.name != 'nt' else 'windows'
    last_output = ""

    while True:
        clear_console()
        print_centered(colorize(banner))
        search_and_tools_banner = combine_banners_side_by_side(
            colorize(banner3), colorize(banner4)
        )
        print_centered(search_and_tools_banner)
        print(colorize(banner2))

        if last_output:
            print("\n" + "=" * 80)
            print(last_output)
            print("=" * 80 + "\n")
            last_output = ""

        prompt_line1 = f"┌──({user_nick}@totem)─[~/{os_name}/{theme_name}]"
        prompt_line2 = "└─$ "
        choice = input(colorize(f"{prompt_line1}\n{prompt_line2}"))

        actions = {
            '1': lookup_phone, '2': track_username, '3': lookup_ip,
            '4': lookup_email, '5': lookup_website, '6': search_local_files,
            '7': search_leak_osint, '8': lookup_vk,
        }
        links = {
            '9': 'https://github.com/Suggika/Requiem-Stealer',
            '10': 'https://github.com/Suggika/Totem-RAT',
            '11': 'https://github.com/n0a/telegram-get-remote-ip',
            '12': 'https://github.com/Suggika/Self-Bot',
        }

        if choice in actions:
            actions[choice]()
            Continue()
        elif choice in links:
            try:
                webbrowser.open(links[choice])
                log_message(INFO, "Открываю ссылку в браузере...")
            except Exception as e:
                log_message(ERROR, f"Не удалось открыть ссылку: {e}")
            Continue()
        elif choice == '99':
            return 100  
        elif choice in ('0', '00'):
            return 0    
        else:
            log_message(ERROR, "Неверный выбор. Пожалуйста, попробуйте снова.")
            time.sleep(2)


if __name__ == "__main__":
    try:
        exit_code = main()
    except KeyboardInterrupt:
        print()
        log_message(INFO, "Программа прервана пользователем. Выход.")
        exit_code = 0
    finally:
        sys.exit(exit_code)

