# ✅ Mega Ultra Library Command System (x20 масштаб, дополнено)
import os
import json
import random

# === Константы ===
COMMAND_COUNT = 20000
BOOKS_FILE = "books.json"
DESCRIPTION = """
🔹 Добро пожаловать в МЕГА-БИБЛИОТЕЧНУЮ КОМАНДНУЮ СИСТЕМУ (версия x20)
Это расширяемая система, способная хранить десятки тысяч команд,
осуществлять поиск по обширной библиотеке книг, и потенциально поддерживать
пользовательские сценарии, фильтрацию, категории, рекомендации и много другое.
"""

# === Генерация данных ===
commands = [f"команда_{i:05}" for i in range(1, COMMAND_COUNT + 1)]
sample_books = [
    {"title": f"Книга по Python {i}", "author": f"Автор {i}", "year": 2000 + i % 20, "genre": random.choice(["Наука", "Программирование", "Фантастика", "Философия"])}
    for i in range(1, 101)
]

# === Сохранение книг ===
if not os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(sample_books, f, indent=4, ensure_ascii=False)

# === Загрузка книг ===
def load_books():
    with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# === Поиск книг ===
def search_books(term):
    books = load_books()
    found = [book for book in books if term.lower() in book['title'].lower() or term.lower() in book['author'].lower() or term.lower() in book['genre'].lower()]
    if found:
        print("\n🔍 Найденные книги:")
        for b in found:
            print(f"📘 {b['title']} — {b['author']} ({b['year']}) | Жанр: {b['genre']}")
    else:
        print("Книги не найдены.")

# === Меню ===
def menu():
    print(DESCRIPTION)
    while True:
        print("\nКоманды: list | command [номер] | search | info | exit")
        cmd = input(">>> ").strip().lower()

        if cmd == "exit":
            break

        elif cmd == "info":
            print(f"\n📊 Всего команд: {COMMAND_COUNT}")
            print("📚 Кол-во книг в библиотеке:", len(load_books()))
            print("🎯 Вы можете искать по названию, автору и жанру.")

        elif cmd == "list":
            print("\n📋 Список первых 200 команд:")
            for i in range(200):
                print(f"{i+1:05}: {commands[i]}")
            print(f"... и ещё {COMMAND_COUNT - 200} команд ...")

        elif cmd.startswith("command"):
            parts = cmd.split()
            if len(parts) == 2 and parts[1].isdigit():
                num = int(parts[1])
                if 1 <= num <= COMMAND_COUNT:
                    print(f"▶️ Выполняется: {commands[num - 1]}...")
                else:
                    print("Номер команды вне диапазона.")
            else:
                print("Неверный формат команды.")

        elif cmd == "search":
            term = input("Введите ключевое слово для поиска книг (название, автор или жанр): ")
            search_books(term)

        else:
            print("Неизвестная команда. Попробуйте снова.")

# === Запуск ===
if __name__ == '__main__':
    menu()