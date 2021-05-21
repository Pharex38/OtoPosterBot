import telebot
import os, signal
import main as anabot

token = "***REMOVED-BOT-TOKEN***"
bot = telebot.TeleBot(token, parse_mode='html')

@bot.message_handler(commands=['start'])
def start(s):
    chat = s.chat.id
    bot.send_message(chat, "Merhaba!")

@bot.message_handler(commands=['run'])
def run(m):
    chat = m.chat.id
    msg = bot.send_message(chat, "<code>Bot yeniden başlatılıyor</code>")
    os.system('main.py')
    bot.send_message(chat, "Yeniden Başlatıldı!")

@bot.message_handler(commands=['stop'])
def stop(p):
    chat = p.chat.id
    os.kill(anabot.pid, signal.SIGKILL)
    bot.send_message(chat, "Bot Durduruldu.")


bot.polling(none_stop=True)