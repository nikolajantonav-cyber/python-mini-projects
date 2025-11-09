
def convert(amount, rate):
    return amount * rate

print("💶 Currency Converter")
amount = float(input("Введите сумму в евро: "))
rate = float(input("Введите курс (например, 1 евро = 1.07 доллара, значит 1.07): "))
print(f"{amount} евро = {convert(amount, rate):.2f} в выбранной валюте 💰")