import telebot
import os, signal
import time

token = "***REMOVED-BOT-TOKEN***"
bot = telebot.TeleBot(token, parse_mode='html')


@bot.message_handler(commands=['start', 'durum'])
def start(s):
    chat = s.chat.id
    pid = open("pid.txt", "r").read()
    if pid.isdigit():
        durum = "Aktif!"
    else:
        durum = "Kapalı!"
    bot.send_message(chat, "Merhaba!\n\nDurum: {}".format(durum))

@bot.message_handler(commands=['run'])
def run(m):
    chat = m.chat.id
    pidd = open("pid.txt", "r+")
    if pidd.read().isdigit():
        islem = os.kill(int(pid), 9)
        time.sleep(1)
        os.system('python main.py')
        bot.send_message(chat, "Yeniden Başlatıldı!")
    os.system('python main.py')
    bot.send_message(chat, "Bot Başlatıldı!")

@bot.message_handler(commands=['stop'])
def stop(p):
    pidd = open("pid.txt", "r+")
    pid = pidd.read()
    chat = p.chat.id
    if pid == "down":
        bot.send_message(chat, "Bot zaten kapalı")
        return
    islem = os.kill(int(pid), 9)
    pidd.write("down")
    bot.send_message(chat, "Bot Durduruldu.")

print("Çalışıyor")

bot.polling(none_stop=True)