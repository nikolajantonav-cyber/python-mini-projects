import tkinter as tk
from tkinter import messagebox, filedialog
import random
import string

settings = {
    "include_uppercase": True,
    "include_numbers": True,
    "include_symbols": True,
    "exclude_similar": False
}

def generate_password():
    length = int(length_entry.get())
    characters = string.ascii_lowercase
    if settings["include_uppercase"]:
        characters += string.ascii_uppercase
    if settings["include_numbers"]:
        characters += string.digits
    if settings["include_symbols"]:
        characters += string.punctuation
    if settings["exclude_similar"]:
        for c in 'il1Lo0O':
            characters = characters.replace(c, '')
    if not characters:
        result_label.config(text="Нет символов для генерации")
        return
    password = ''.join(random.choice(characters) for _ in range(length))
    result_label.config(text=password)

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(result_label.cget("text"))
    root.update()
    messagebox.showinfo("Copied", "Скопировано!")

def save_to_file():
    pw = result_label.cget("text")
    if not pw:
        messagebox.showwarning("Warning", "Сначала сгенерируй пароль")
        return
    path = filedialog.asksaveasfilename(defaultextension=".txt")
    if path:
        with open(path, 'w') as f:
            f.write(pw)
        messagebox.showinfo("Saved", f"Пароль сохранён в {path}")

def toggle_setting(name):
    settings[name] = not settings[name]
    update_labels()

def update_labels():
    uc_btn.config(text=f"Uppercase: {'ON' if settings['include_uppercase'] else 'OFF'}")
    num_btn.config(text=f"Numbers: {'ON' if settings['include_numbers'] else 'OFF'}")
    sym_btn.config(text=f"Symbols: {'ON' if settings['include_symbols'] else 'OFF'}")
    sim_btn.config(text=f"Exclude Similar: {'ON' if settings['exclude_similar'] else 'OFF'}")

root = tk.Tk()
root.title("Password Generator")
root.geometry("400x350")

tk.Label(root, text="Password Length:").pack()
length_entry = tk.Entry(root)
length_entry.pack()
length_entry.insert(0, "12")

tk.Button(root, text="Generate", command=generate_password).pack(pady=5)
result_label = tk.Label(root, text="", font=("Courier", 14))
result_label.pack()
tk.Button(root, text="Copy", command=copy_to_clipboard).pack(pady=5)
tk.Button(root, text="Save to File", command=save_to_file).pack(pady=5)

uc_btn = tk.Button(root, command=lambda: toggle_setting("include_uppercase"))
uc_btn.pack()
num_btn = tk.Button(root, command=lambda: toggle_setting("include_numbers"))
num_btn.pack()
sym_btn = tk.Button(root, command=lambda: toggle_setting("include_symbols"))
uc_btn.pack()
sim_btn = tk.Button(root, command=lambda: toggle_setting("exclude_similar"))
sim_btn.pack()
update_labels()

root.mainloop()


