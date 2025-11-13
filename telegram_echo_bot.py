from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
import logging

TOKEN = '"""""'

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Команды
user_messages = []

def start(update, context):
    update.message.reply_text('Привет! Я простой бот. Напиши /help, чтобы узнать, что я умею.')

def help_command(update, context):
    update.message.reply_text('/start - начать\n/help - помощь\n/info - информация\n/log - последние сообщения')

def info(update, context):
    update.message.reply_text('Я echo-бот, созданный на Python. Я могу повторять твои сообщения и хранить лог.')

def echo(update, context):
    msg = update.message.text
    user_messages.append(f"{datetime.now().strftime('%H:%M:%S')} - {msg}")
    update.message.reply_text(f"Ты написал: {msg}")

def show_log(update, context):
    if user_messages:
        update.message.reply_text("Последние сообщения:\n" + "\n".join(user_messages[-5:]))
    else:
        update.message.reply_text("Нет сохранённых сообщений.")

def unknown(update, context):
    update.message.reply_text("Извините, я не понимаю эту команду.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('info', info))
    dp.add_handler(CommandHandler('log', show_log))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()