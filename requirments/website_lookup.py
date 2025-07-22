import socket
import whois
import requests
from datetime import datetime
from config import *

def format_date(date_obj):
    if not date_obj:
        return "Нет данных"
    if isinstance(date_obj, list):
        date_obj = date_obj[0]
    if isinstance(date_obj, datetime):
        return date_obj.strftime('%d-%m-%Y %H:%M:%S')
    return str(date_obj)

def lookup_website():
    Title("Поиск информации о сайте")
    try:
        print(colorize(Website))
        domain = input(get_prompt("Введите домен сайта (например, google.com)"))
        log_message(INFO, f"Идет поиск по запросу: {domain}")
        log_message(WAIT, "Получение информации...")

        try:
            ip_address = socket.gethostbyname(domain)
        except socket.gaierror:
            ip_address = "Не удалось определить"

        try:
            w = whois.whois(domain)
            registrar = w.registrar or "Нет данных"
            creation_date = format_date(w.creation_date)
            expiration_date = format_date(w.expiration_date)
        except (whois.parser.PywhoisError, AttributeError):
            registrar, creation_date, expiration_date = "Нет данных", "Нет данных", "Нет данных"
        
        try:
            response = requests.get(f"https://{domain}", timeout=5, allow_redirects=True)
            server_header = response.headers.get('Server', 'Не определен')
        except requests.RequestException:
            server_header = "Не удалось подключиться"

        Slow(f"""
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {ADD} Домен: {domain}
 {ADD} IP Адрес: {ip_address}
 {ADD} Сервер: {server_header}
 {ADD} Регистратор: {registrar}
 {ADD} Дата создания: {creation_date}
 {ADD} Дата окончания: {expiration_date}
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
""")

    except Exception as e:
        Error(e)
