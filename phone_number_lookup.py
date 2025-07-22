import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from config import *

def lookup_phone():
    Title("Поиск по номеру телефона")
    try:
        print(colorize(Phone))
        phone_number = input(get_prompt("Введите номер телефона"))
        log_message(WAIT, "Получение информации...")
        
        parsed_number = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            log_message(INFO, "Неверный формат номера!")
            return

        status = "Валид" if phonenumbers.is_valid_number(parsed_number) else "Невалид"
        country_code = f"+{parsed_number.country_code}"
        operator = carrier.name_for_number(parsed_number, "ru") or "Не определен"
        type_number = "Мобильный" if phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE else "Стационарный"
        timezones = timezone.time_zones_for_number(parsed_number)
        timezone_info = timezones[0] if timezones else "Не определена"
        country = phonenumbers.region_code_for_number(parsed_number)
        region = geocoder.description_for_number(parsed_number, "ru") or "Не определен"
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)

        Slow(f"""
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {ADD} Номер: {phone_number}
 {ADD} Статус: {status}
 {ADD} Код страны: {country_code}
 {ADD} Страна: {country}
 {ADD} Регион: {region}
 {ADD} Часовой пояс: {timezone_info}
 {ADD} Оператор: {operator}
 {ADD} Тип номеh: {type_number}
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
""")

    except phonenumbers.phonenumberutil.NumberParseException as e:
        log_message(ERROR, f"Ошибка анализа номера: {e}. Убедитесь, что номер в международном формате (например, +79991234567).")
    except Exception as e:
        Error(e)
