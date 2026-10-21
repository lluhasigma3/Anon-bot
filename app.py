import os
import threading
from flask import Flask
import telebot

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
YOUR_CHAT_ID = os.environ.get("YOUR_CHAT_ID")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Напиши свой вопрос, и админ ответит тебе.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    username = message.from_user.username or "Нет юзернейма"
    text = message.text

    # Если пишет сам админ (ты) и использует команду /reply
    if str(message.chat.id) == str(YOUR_CHAT_ID) and text.startswith('/reply'):
        try:
            parts = text.split(' ', 2)
            target_id = parts[1]
            reply_text = parts[2]
            
            bot.send_message(target_id, f"👑 **Ответ от админа:**\n\n{reply_text}", parse_mode='Markdown')
            bot.reply_to(message, "✅ Ответ отправлен!")
        except:
            bot.reply_to(message, "⚠️ Ошибка. Пиши так: /reply ID текст")
        return

    # Если пишет обычный пользователь
    admin_msg = f"📩 Новое сообщение!\n\n👤 От: {username}\n🆔 ID: `{user_id}`\n\n💬 Текст:\n{text}\n\n✍️ Ответить: `/reply {user_id} твой_текст`"
    
    try:
        bot.send_message(YOUR_CHAT_ID, admin_msg, parse_mode='Markdown')
        bot.reply_to(message, "✅ Сообщение отправлено! Жди ответа.")
    except Exception as e:
        bot.reply_to(message, "⚠️ Ошибка: админ недоступен.")

@app.route('/')
def health():
    return "Bot is running!"

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
