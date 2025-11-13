import os
import json
import datetime
import random

DATA_DIR = "chat_data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
MESSAGES_FILE = os.path.join(DATA_DIR, "messages.json")
BLOCKS_FILE = os.path.join(DATA_DIR, "blocked.json")

os.makedirs(DATA_DIR, exist_ok=True)

# === Основные операции с JSON ===
def load(file, default):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default

def save(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# === Регистрация и статус ===
def register(username):
    users = load(USERS_FILE, {})
    if username not in users:
        users[username] = {
            "status": "online",
            "avatar": f"avatar_{random.randint(1,5)}.png",
            "draft": ""
        }
        save(USERS_FILE, users)
        print(f"Пользователь {username} зарегистрирован.")
    else:
        users[username]["status"] = "online"
        save(USERS_FILE, users)

# === Блокировка пользователей ===
def block_user(by, target):
    blocks = load(BLOCKS_FILE, {})
    if by not in blocks:
        blocks[by] = []
    if target not in blocks[by]:
        blocks[by].append(target)
        save(BLOCKS_FILE, blocks)
        print(f"{target} заблокирован.")

def is_blocked(sender, receiver):
    blocks = load(BLOCKS_FILE, {})
    return receiver in blocks.get(sender, [])

# === Черновики ===
def save_draft(username, text):
    users = load(USERS_FILE, {})
    if username in users:
        users[username]["draft"] = text
        save(USERS_FILE, users)

def show_draft(username):
    users = load(USERS_FILE, {})
    return users.get(username, {}).get("draft", "")

# === Сообщения ===
def send_message(from_user, to_user, text):
    if is_blocked(to_user, from_user):
        print(f"Вы не можете отправить сообщение {to_user}. Вы в черном списке.")
        return
    messages = load(MESSAGES_FILE, [])
    msg = {
        "from": from_user,
        "to": to_user,
        "text": text,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    messages.append(msg)
    save(MESSAGES_FILE, messages)
    print(f"📨 Сообщение отправлено {to_user}.")

def read_messages(username):
    messages = load(MESSAGES_FILE, [])
    received = [m for m in messages if m['to'] == username]
    if not received:
        print("У вас нет новых сообщений.")
    for m in received:
        print(f"[{m['time']}] {m['from']}: {m['text']}")

# === Статус пользователей ===
def show_users():
    users = load(USERS_FILE, {})
    for name, info in users.items():
        print(f"👤 {name} | Статус: {info['status']} | Аватар: {info['avatar']}")

# === Главный интерфейс ===
def chat():
    username = input("Введите имя пользователя: ")
    register(username)
    while True:
        print("
Команды: users | send | read | block | draft | show_draft | exit")
        cmd = input(">>> ").strip().lower()
        if cmd == "users":
            show_users()
        elif cmd == "send":
            to = input("Кому: ")
            msg = input("Сообщение: ")
            send_message(username, to, msg)
        elif cmd == "read":
            read_messages(username)
        elif cmd == "block":
            user_to_block = input("Кого заблокировать: ")
            block_user(username, user_to_block)
        elif cmd == "draft":
            draft_text = input("Введите черновик: ")
            save_draft(username, draft_text)
        elif cmd == "show_draft":
            print(f"Черновик: {show_draft(username)}")
        elif cmd == "exit":
            break
        else:
            print("Неизвестная команда.")

if __name__ == '__main__':
    chat()