import telebot
import os

token = "***REMOVED-BOT-TOKEN***"
bot = telebot.TeleBot(token, parse_mode='html')

@bot.message_handler(commands=['start'])
def start(s):
    chat = s.chat.id
    bot.send_message(chat, "Merhaba")

@bot.message_handler(commands=['run'])
def run(m):
    chat = m.chat.id
    msg = bot.send_message(chat, "<code>Bot yeniden başlatılıyor</code>")
    os.system('python main.py')
    bot.edit_text_message(chat, msg.message_id, "Yeniden Başlatıldı!")


bot.polling(none_stop=True)