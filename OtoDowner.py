import telebot
import os, signal

token = "***REMOVED-BOT-TOKEN***"
bot = telebot.TeleBot(token, parse_mode='html')

pid = open("pid.txt", "r").read()

@bot.message_handler(commands=['start'])
def start(s):
    chat = s.chat.id
    bot.send_message(chat, "Merhaba!")

@bot.message_handler(commands=['run'])
def run(m):
    chat = m.chat.id
    msg = bot.send_message(chat, "<code>Bot yeniden başlatılıyor</code>")
    os.system('python main.py')
    bot.send_message(chat, "Yeniden Başlatıldı!")

@bot.message_handler(commands=['stop'])
def stop(p):
    chat = p.chat.id
    islem = os.kill(int(pid), 9)
    print(islem)
    bot.send_message(chat, "Bot Durduruldu.")

print("Çalışıyor")

bot.polling(none_stop=True)