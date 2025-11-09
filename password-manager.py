import json
from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet = Fernet(key)

def save_password(service, password):
    data = {}
    try:
        with open("passwords.json", "r") as f:
            data = json.load(f)
    except:
        pass

    data[service] = fernet.encrypt(password.encode()).decode()

    with open("passwords.json", "w") as f:
        json.dump(data, f)

def view_passwords():
    try:
        with open("passwords.json", "r") as f:
            data = json.load(f)
        for s, p in data.items():
            print(f"{s}: {fernet.decrypt(p.encode()).decode()}")
    except:
        print("Нет сохранённых паролей")

while True:
    act = input("(a)dd, (v)iew, (q)uit: ")
    if act == 'a':
        save_password(input("Сервис: "), input("Пароль: "))
    elif act == 'v':
        view_passwords()
    else:
        break