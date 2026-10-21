import os
import threading
from flask import Flask
import telebot

TELEGRAM_TOKEN = "8892707247:AAER1fzuVWRXHEWzohnt48jwcbcIMCCxF9E"
YOUR_CHAT_ID = "8028897913"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Это бот сообщения по Counter Flame Upgrader. Тут ты можешь написать сообщение админу, и есть шанс, что твою идею примут.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    username = message.from_user.username or "Нет"
    text = message.text

    if str(message.chat.id) == str(YOUR_CHAT_ID) and text.startswith('/reply'):
        try:
            parts = text.split(' ', 2)
            bot.send_message(parts[1], f"Ответ от админа: {parts[2]}")
            bot.reply_to(message, "Отправлено!")
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {e}")
        return

    admin_msg = f"Сообщение от {username} (ID: {user_id}):\n{text}\n\nОтвет: /reply {user_id} текст"
    
    try:
        bot.send_message(YOUR_CHAT_ID, admin_msg)
        bot.reply_to(message, "Отправлено!")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

@app.route('/')
def health():
    return "OK"

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
