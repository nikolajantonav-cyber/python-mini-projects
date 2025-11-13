import requests
import time
import json
import os
from datetime import datetime

API_KEY = 'YOUR_API_KEY'
BASE_URL = 'https://v6.exchangerate-api.com/v6'
HISTORY_FILE = 'conversion_history.json'
FAVORITES_FILE = 'favorite_currencies.json'

# --- Конвертация валют ---
def convert(from_currency, to_currency, amount):
    url = f"{BASE_URL}/{API_KEY}/pair/{from_currency}/{to_currency}/{amount}"
    try:
        r = requests.get(url)
        data = r.json()
        if data['result'] == 'success':
            result = data['conversion_result']
            print(f"{amount} {from_currency} = {result} {to_currency}")
            log_conversion(from_currency, to_currency, amount, result)
        else:
            print("Ошибка конвертации:", data.get("error-type"))
    except Exception as e:
        print("Ошибка соединения:", e)

# --- История ---
def log_conversion(from_cur, to_cur, amount, result):
    history = load_json(HISTORY_FILE)
    record = {
        "from": from_cur,
        "to": to_cur,
        "amount": amount,
        "result": result,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    history.append(record)
    save_json(HISTORY_FILE, history)

def show_history():
    history = load_json(HISTORY_FILE)
    if not history:
        print("История пуста.")
        return
    print("Последние 10 операций:")
    for h in history[-10:]:
        print(f"{h['timestamp']}: {h['amount']} {h['from']} => {h['result']} {h['to']}")

# --- Избранные валюты ---
def add_favorite():
    favorites = load_json(FAVORITES_FILE)
    pair = input("Введите пару валют (например, USD->EUR): ")
    if pair not in favorites:
        favorites.append(pair)
        save_json(FAVORITES_FILE, favorites)
        print("Добавлено в избранное.")
    else:
        print("Такая пара уже есть.")

def show_favorites():
    favorites = load_json(FAVORITES_FILE)
    if not favorites:
        print("Нет избранных пар.")
        return
    print("Избранные валюты:")
    for pair in favorites:
        parts = pair.split("->")
        if len(parts) == 2:
            convert(parts[0], parts[1], 1)

# --- JSON utils ---
def load_json(file):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Меню ---
def menu():
    while True:
        print("\n1. Конвертировать валюту\n2. История\n3. Избранное\n4. Добавить в избранное\n5. Выход")
        choice = input("Выбор: ")
        if choice == '1':
            from_cur = input("Из валюты: ").upper()
            to_cur = input("В валюту: ").upper()
            try:
                amt = float(input("Сумма: "))
                convert(from_cur, to_cur, amt)
            except:
                print("Некорректная сумма.")
        elif choice == '2':
            show_history()
        elif choice == '3':
            show_favorites()
        elif choice == '4':
            add_favorite()
        elif choice == '5':
            break
        else:
            print("Неверный выбор.")

if __name__ == '__main__':
    menu()