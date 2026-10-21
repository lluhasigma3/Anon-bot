import os
import threading
from flask import Flask
import telebot

# Берем токен из настроек Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8635648695:AAHellwCa4K5NKxcQ3EZ0NVBLmlEf48NSxk")
YOUR_CHAT_ID = os.environ.get("YOUR_CHAT_ID", "8028897913") # Твой ID вставлен сюда

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Напиши свой вопрос или сообщение, и оно улетит админу.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    username = message.from_user.username or "Без юзернейма"
    first_name = message.from_user.first_name or "Аноним"
    text = message.text

    admin_msg = f"📩 Новое сообщение!\n\n👤 От: {first_name} (@{username})\n🆔 ID: {user_id}\n\n💬 Текст:\n{text}"
    
    try:
        bot.send_message(YOUR_CHAT_ID, admin_msg)
        bot.reply_to(message, "✅ Сообщение отправлено!")
    except Exception as e:
        bot.reply_to(message, "⚠️ Ошибка: админ не настроил бота.")

@app.route('/')
def health():
    return "Bot is running!"

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
