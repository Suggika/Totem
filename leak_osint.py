import requests
import webbrowser
import os
from config import *

def escape_html(text):
    if not isinstance(text, str):
        text = str(text)
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#39;"))

def create_and_open_html_report(data, query):
    collections = data.get('List', {})
    total_collections = len(collections)
    total_results = sum(info.get('NumOfResults', 0) for info in collections.values())

    html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Результаты поиска для: {escape_html(query)}</title>
  <style>
    body {{
      margin: 0; padding: 0;
      font-family: ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
      background-color: #0d1117; color: #c9d1d9;
      text-align: center;
    }}
    .header {{
      background-color: #161b22; padding: 1rem;
      font-size: 1.25rem; font-weight: 600;
      border-bottom: 1px solid #30363d;
    }}
    .container {{
      max-width: 900px; margin: 2rem auto;
      background-color: #161b22; padding: 2rem;
      border: 1px solid #30363d;
      border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.5);
      text-align: left;
    }}
    h1 {{ font-size: 1.75rem; margin-bottom: 1rem; text-align: center;}}
    .info {{ font-size: 1.1rem; margin: 0.5rem 0; text-align: center;}}
    .collection {{
      background-color: #0d1117; padding: 1.5rem;
      border: 1px solid #30363d;
      border-radius: 8px; margin: 1.5rem 0;
    }}
    .title {{ font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem; color: #58a6ff;}}
    ul {{ list-style: none; padding: 0; margin: 1rem 0; }}
    li {{
        background-color: #161b22;
        padding: 0.75rem;
        border-left: 3px solid #58a6ff;
        margin-bottom: 0.5rem;
        word-wrap: break-word;
    }}
    li strong {{ color: #a5d6ff; }}
    hr {{ border-color: #30363d; margin: 2rem 0;}}
  </style>
</head>
<body>
  <div class="header">
    Результаты поиска Totem
  </div>
  <div class="container">
    <h1>Запрос: "{escape_html(query)}"</h1>
    <p class="info"><strong>Коллекций:</strong> {total_collections}</p>
    <p class="info"><strong>Всего результатов:</strong> {total_results}</p>
    <hr>
"""

    for name, info in collections.items():
        html_content += f"""
    <div class="collection">
      <div class="title">{escape_html(name)}</div>
      <p class="info">Найдено: {info.get('NumOfResults', 0)}</p>
      <ul>
"""
        for entry in info.get('Data', []):
            html_content += "        <li>" + "<br>".join(
                f"<strong>{escape_html(k)}:</strong> {escape_html(v)}"
                for k, v in entry.items()
            ) + "</li>\n"
        html_content += "      </ul>\n    </div>\n"

    html_content += """
  </div>
</body>
</html>
"""

    filename = "leak_osint_results.html"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        full_path = os.path.abspath(filename)
        webbrowser.open('file://' + full_path)
        log_message(INFO, f"Результаты сохранены в файл {filename} и открыты в браузере.")

    except Exception as e:
        log_message(ERROR, f"Не удалось создать или открыть HTML-файл: {e}")


def search_leak_osint():
    Title("Поиск утечек")
    print(colorize(Osint))
    log_message(INFO, "Поиск по API leakosintapi.com | Если у тебя нет ключа перейди в чат @suggika там тебе помогут")

    try:
        api_key = input(get_prompt("Введи API ключ:"))
        if not api_key:
            log_message(ERROR, "API ключ не может быть пустым.")
            return

        query = input(get_prompt("Введите запрос:"))
        if not query:
            log_message(ERROR, "Запрос не может быть пустым.")
            return

        log_message(WAIT, "Отправка запроса к API...")
        
        url = 'https://leakosintapi.com/'
        data = {
            "token": api_key,
            "request": query,
            "limit": 200,
            "lang": "ru"
        }
        
        response = requests.post(url, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()

        if isinstance(result, dict) and result.get('List'):
            log_message(INFO, "Данные получены, генерируется HTML-отчет...")
            create_and_open_html_report(result, query)
        elif isinstance(result, dict) and 'error' in result:
             log_message(ERROR, f"API вернул ошибку: {result['error']}")
        else:
            log_message(INFO, "По вашему запросу ничего не найдено или получен некорректный ответ.")
            print(result)

    except requests.exceptions.HTTPError as http_err:
        log_message(ERROR, f"HTTP ошибка: {http_err}")
    except requests.exceptions.RequestException as e:
        log_message(ERROR, f"Ошибка сети: {e}")
    except Exception as e:
        Error(e)
