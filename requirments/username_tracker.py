import requests
import time
from config import *
from social_sites import sites

def track_username():
    Title("Поиск по юзу")
    try:
        user_agent = ChoiceUserAgent()
        headers = {"User-Agent": user_agent}
        number_site = 0
        number_found = 0
        sites_and_urls_found = []
        print(colorize(Username))
        username = input(get_prompt("Введите никнейм")).lower()
        log_message(INFO, f"Идет поиск по запросу: {username}")
        log_message(WAIT, "Сканирование...")

        session = requests.Session()

        for site, data in sites.items():
            number_site += 1
            url = data["url"].format(username=username)
            try:
                response = session.get(url, timeout=10, headers=headers)
                if response.status_code == 200 and data["error_text"] not in response.text:
                    number_found += 1
                    sites_and_urls_found.append({site: url})
                    print(f"[+] {site}: {url}")
                else:
                    print(f"[-] {site}: Не найдено")
            except requests.exceptions.RequestException:
                print(f"[x] {site}: Ошибка подключения")

        if number_found > 0:
            print(f"\nВсего найдено:")
            for site_and_url_found in sites_and_urls_found:
                for site, url in site_and_url_found.items():
                    time.sleep(0.1)
                    print(f"────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────")
                    print(f"{ADD} Сайт: {site}")
                    print(f"{ADD} Ссылка: {url}")
            print(f"────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────")

        log_message(INFO, f"Всего сайтов: {number_site} | Всего найдено: {number_found}")

    except Exception as e:
        Error(e)
