
import random

print("🎲 Угадай число!")
secret = random.randint(1, 20)
attempts = 0

while True:
    guess = int(input("Введи число от 1 до 20: "))
    attempts += 1
    if guess < secret:
        print("Больше 🔼")
    elif guess > secret:
        print("Меньше 🔽")
    else:
        print(f"🔥 Угадал! Это {secret}. Попыток: {attempts}")
        break