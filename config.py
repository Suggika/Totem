import time
import sys
import os
from datetime import datetime

ANSI_COLORS = {
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "PURPLE": "\033[95m",
    "CYAN": "\033[96m",
    "WHITE": "\033[97m",
    "AMBER": "\033[93m",
    "BROWN": "\033[33m",
    "DEEP_ORANGE": "\033[31m",
    "ORANGE": "\033[33m",
    "INDIGO": "\033[34m",
    "PINK": "\033[95m",
    "TEAL": "\033[36m",
    "LIME": "\033[92m",
    "LIGHT_GREEN": "\033[92m",
    "LIGHT_BLUE": "\033[94m",
    "DEEP_PURPLE": "\033[35m",
}
ANSI_RESET = "\033[0m"
CURRENT_THEME_COLOR = ANSI_RESET

def set_theme(theme_name):
    global CURRENT_THEME_COLOR
    theme_name_upper = theme_name.upper()
    best_match = ""
    for key in ANSI_COLORS:
        if key in theme_name_upper:
            if len(key) > len(best_match):
                best_match = key
    if best_match:
        CURRENT_THEME_COLOR = ANSI_COLORS[best_match]
    else:
        CURRENT_THEME_COLOR = ANSI_COLORS["WHITE"]

def colorize(text, color_code=None):
    color = color_code if color_code else CURRENT_THEME_COLOR
    return f"{color}{text}{ANSI_RESET}"

INPUT = colorize("[>]")
INFO = colorize("[!]")
WAIT = colorize("[~]")
ERROR = colorize("[x]", ANSI_COLORS.get("RED"))
ADD = colorize("[+]")

def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

def get_prompt(prompt_text):
    return f"\n{colorize(f'[{current_time_hour()}]')} {INPUT} | {prompt_text} -> "

def log_message(symbol, message):
    print(f"{colorize(f'[{current_time_hour()}]')} {symbol} | {message}")

def Slow(text):
    sys.stdout.write(CURRENT_THEME_COLOR)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.005)
    sys.stdout.write(ANSI_RESET)
    print()

def Title(text):
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80
    padding_char = colorize("=")
    padding_len = (terminal_width - len(text) - 2) // 2
    padding_str = padding_char * padding_len
    print("\n" + padding_str + f" {colorize(text)} " + padding_str + "\n")

def Error(e):
    error_color = ANSI_COLORS.get("RED", "\033[91m")
    print(f"{colorize(f'[{current_time_hour()}]', error_color)} {colorize('[x]', error_color)} | {colorize(f'Произошла ошибка: {e}', error_color)}")
    Continue()
    Reset()

def Continue():
    input(f"\n{INPUT} Нажмите Enter, чтобы продолжить...")

def Reset():
    print("\n" + colorize("="*50) + "\n")

def ChoiceUserAgent():
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
Phone = r"""
    ____  __                   
   / __ \/ /_  ____  ____  ___ 
  / /_/ / __ \/ __ \/ __ \/ _ \
 / ____/ / / / /_/ / / / /  __/
/_/   /_/ /_/\____/_/ /_/\___/              
"""
Osint = r"""   
   ____       _       __ 
  / __ \_____(_)___  / /_
 / / / / ___/ / __ \/ __/
/ /_/ (__  ) / / / / /_  
\____/____/_/_/ /_/\__/  
                         
"""
Email = r"""
    ______                _ __
   / ____/___ ___  ____ _(_) /
  / __/ / __ `__ \/ __ `/ / / 
 / /___/ / / / / / /_/ / / /  
/_____/_/ /_/ /_/\__,_/_/_/   
                              
"""
Ip = r"""
    ________ 
   /  _/ __ \
   / // /_/ /
 _/ // ____/ 
/___/_/      
             
"""
Database = r"""
    ____        __        __                  
   / __ \____ _/ /_____ _/ /_  ____ _________ 
  / / / / __ `/ __/ __ `/ __ \/ __ `/ ___/ _ \
 / /_/ / /_/ / /_/ /_/ / /_/ / /_/ (__  )  __/
/_____/\__,_/\__/\__,_/_.___/\__,_/____/\___/ 
                                              
"""
Username = r"""
   __  __                                        
  / / / /_______  _________  ____ _____ ___  ___ 
 / / / / ___/ _ \/ ___/ __ \/ __ `/ __ `__ \/ _ \
/ /_/ (__  )  __/ /  / / / / /_/ / / / / / /  __/
\____/____/\___/_/  /_/ /_/\__,_/_/ /_/ /_/\___/ 
                                                 
"""
Website = r"""
 _       __     __         _ __     
| |     / /__  / /_  _____(_) /____ 
| | /| / / _ \/ __ \/ ___/ / __/ _ \
| |/ |/ /  __/ /_/ (__  ) / /_/  __/
|__/|__/\___/_.___/____/_/\__/\___/ 
                                    
"""
VK = r"""
 _    ____ __
| |  / / //_/
| | / / ,<   
| |/ / /| |  
|___/_/ |_|  
             
"""