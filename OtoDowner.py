import telebot
import os, signal
import time

token = "***REMOVED-BOT-TOKEN***"
bot = telebot.TeleBot(token, parse_mode='html')

yetkili = [1613760981, 755051086, 1302980840]

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
    pid = pidd.read()
    if pid.isdigit():
        islem = os.kill(int(pid), 9)
        time.sleep(1)
        bot.send_message(chat, "Yeniden Başlatıldı!")
        os.system('python main.py')
        return
    bot.send_message(chat, "Bot Başlatıldı!")
    os.system('python main.py')

@bot.message_handler(commands=['stop'])
def stop(p):
    pidd = open("pid.txt", "r+")
    pid = pidd.read()
    chat = p.chat.id
    if pid == "down":
        bot.send_message(chat, "Bot zaten kapalı")
        return
    try:
        islem = os.kill(int(pid), 9)
    except Exception as e:
        print(e)
    pidd.write("down")
    bot.send_message(chat, "Bot Durduruldu.")

print("Çalışıyor")

bot.polling(none_stop=True)