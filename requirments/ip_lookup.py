import requests
from config import *

def lookup_ip():
    Title("Поиск по IP")
    try:
        print(colorize(Ip))
        ip = input(get_prompt("Введите IP адрес"))
        log_message(WAIT, "Поиск информации...")

        response = requests.get(f"http://ip-api.com/json/{ip}")
        api = response.json()

        if api.get('status') == "fail":
            log_message(ERROR, f"Не удалось найти информацию для IP: {ip}. Причина: {api.get('message')}")
            return

        status = "Действительный" if api.get('status') == "success" else "Недействительный"
        country = api.get('country', "Нет данных")
        country_code = api.get('countryCode', "Нет данных")
        region = api.get('regionName', "Нет данных")
        zip_code = api.get('zip', "Нет данных")
        city = api.get('city', "Нет данных")
        latitude = api.get('lat', "Нет данных")
        longitude = api.get('lon', "Нет данных")
        timezone = api.get('timezone', "Нет данных")
        isp = api.get('isp', "Нет данных")
        org = api.get('org', "Нет данных")
        as_host = api.get('as', "Нет данных")

        Slow(f"""
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {ADD} Статус: {status}
 {ADD} Страна: {country} ({country_code})
 {ADD} Регион: {region}
 {ADD} Индекc: {zip_code}
 {ADD} Город: {city}
 {ADD} Широта: {latitude}
 {ADD} Долгота: {longitude}
 {ADD} Часовой пояс: {timezone}
 {ADD} Провайдер: {isp}
 {ADD} Организация: {org}
 {ADD} AS: {as_host}
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
""")

    except requests.exceptions.RequestException as e:
        log_message(ERROR, f"Ошибка сети: {e}")
    except Exception as e:
        Error(e)
