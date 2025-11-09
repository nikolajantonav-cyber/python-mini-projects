
print("📋 Твой планировщик задач")
tasks = []

while True:
    action = input("(a)dd, (v)iew, (q)uit: ")
    if action == "a":
        task = input("Добавь задачу: ")
        tasks.append(task)
        print("✅ Добавлено!")
    elif action == "v":
        print("\nСписок задач:")
        for i, t in enumerate(tasks, 1):
            print(f"{i}. {t}")
    elif action == "q":
        print("До встречи!")
        break
    else:
        print("Неизвестная команда")