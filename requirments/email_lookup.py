import dns.resolver
import re
from config import *

def lookup_email():
    Title("Поиск по почте")
    try:
        print(colorize(Email))
        email = input(get_prompt("Введите Email"))
        log_message(INFO, f"Идет поиск по запросу: {email}")
        log_message(WAIT, "Получение информации...")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            log_message(ERROR, "Неверный формат Email.")
            return

        domain_all = email.split('@')[-1]
        name = email.split('@')[0]
        
        info = {}
        try:
            mx_records = dns.resolver.resolve(domain_all, 'MX')
            info["mx_servers"] = sorted([str(record.exchange) for record in mx_records])
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            info["mx_servers"] = ["Не найдено"]
        
        try:
            txt_records = dns.resolver.resolve(domain_all, 'TXT')
            info["spf_records"] = [str(r) for r in txt_records if 'spf1' in str(r).lower()] or ["Не найдено"]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            info["spf_records"] = ["Не найдено"]

        try:
            dmarc_records = dns.resolver.resolve(f'_dmarc.{domain_all}', 'TXT')
            info["dmarc_records"] = [str(r) for r in dmarc_records] or ["Не найдено"]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            info["dmarc_records"] = ["Не найдено"]

        Slow(f"""
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {ADD} Email: {email}
 {ADD} Имя: {name}
 {ADD} Домен: {domain_all}
 {ADD} MX Серверы: {', '.join(info['mx_servers'])}
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
""")

    except Exception as e:
        Error(e)
