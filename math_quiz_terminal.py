import random
import time
import json
import os

SCORES_FILE = 'quiz_scores.json'
QUESTION_FILE = 'questions.json'

DIFFICULTY = {
    "easy": (1, 10),
    "medium": (10, 30),
    "hard": (30, 100)
}

def generate_question(level):
    a = random.randint(*DIFFICULTY[level])
    b = random.randint(*DIFFICULTY[level])
    op = random.choice(['+', '-', '*'])
    question = f"{a} {op} {b}"
    answer = eval(question)
    return question, answer

def save_score(name, score):
    scores = load_scores()
    scores.append({"name": name, "score": score, "time": time.ctime()})
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=4)

def load_scores():
    try:
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def custom_questions():
    if not os.path.exists(QUESTION_FILE):
        return []
    with open(QUESTION_FILE, 'r') as f:
        return json.load(f)

def add_custom_question():
    q = input("Введите свой вопрос (например: 5 + 3): ")
    try:
        a = eval(q)
        questions = custom_questions()
        questions.append({"q": q, "a": a})
        with open(QUESTION_FILE, 'w') as f:
            json.dump(questions, f, indent=4)
        print("Вопрос добавлен.")
    except:
        print("Некорректный вопрос.")

def show_scores():
    scores = load_scores()
    print("\nПоследние результаты:")
    for s in scores[-5:]:
        print(f"{s['name']}: {s['score']} баллов ({s['time']})")

def quiz():
    name = input("Твоё имя: ")
    level = input("Сложность (easy, medium, hard): ").lower()
    if level not in DIFFICULTY:
        level = "easy"
    score = 0
    questions = [generate_question(level) for _ in range(7)]
    questions += [(q['q'], q['a']) for q in custom_questions()[:3]]
    random.shuffle(questions)
    for i, (q, a) in enumerate(questions):
        try:
            user = int(input(f"Вопрос {i+1}: {q} = "))
            if user == a:
                print("✅ Верно!")
                score += 1
            else:
                print(f"❌ Неверно! Ответ: {a}")
        except:
            print(f"⚠️ Неверный ввод. Ответ был: {a}")
    print(f"Результат: {score}/{len(questions)}")
    save_score(name, score)
    show_scores()

if __name__ == '__main__':
    while True:
        print("\nМеню: quiz | add | exit")
        cmd = input("Выбор: ").strip().lower()
        if cmd == "quiz":
            quiz()
        elif cmd == "add":
            add_custom_question()
        elif cmd == "exit":
            break
        else:
            print("Неверная команда.")
