import telebot
import os, signal
import logging
import Colorer
import psutil
import time, datetime
import threading

token = "***REMOVED-BOT-TOKEN***"

yetkili = [1613760981, 755051086, 1302980840]

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",level=logging.INFO)
logs = logging.getLogger(__name__)

bot = telebot.TeleBot(token,parse_mode='html')

def is_running():
    anapid = open("pid.txt", "r+").read()
    for q in psutil.process_iter():
        if q.name().startswith('python'):
            if q.pid == int(anapid):
                logs.info("İşlem hâlâ çalışıyor.")
                return True
    logs.warning("İşlem Bulunamadı.")
    return False

def kontrol():
    while True:
        time.sleep(60)
        if not is_running():
            bot.send_message(1302980840, "Bot çöktü!")


eskipidfile = open("dpid.txt", "r+")
eskipid = eskipidfile.read()
anapid = open("pid.txt", "r+").read()
try:
    os.kill(int(eskipid), 9)
except Exception as e:
    print(e)
try:
    os.kill(int(anapid), 9)
except Exception as e:
    print("ikinci: {}".format(e))
else:
    os.startfile("basla.bat")
logs.info("Eski İşlem Kapatıldı")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat = message.chat.id
    pid = open("pid.txt", "r").read()
    if is_running():
        durum = "Aktif!"
    else:
        durum = "Kapalı!"
    bot.send_message(chat, "Merhaba!\n\nDurum: {}".format(durum))

@bot.message_handler(commands=['run'])
def run(message):
    chat = message.chat.id
    user = message.from_user.id
    if not user in yetkili:
        bot.send_message(chat, "Bunu yapmak için yetkili değilsiniz!")
        return
    pidd = open("pid.txt", "r+")
    pid = pidd.read()
    if pid.isdigit():
        try:
            islem = os.kill(int(pid), 9)
        except:
            pass
        time.sleep(1)
        os.startfile('basla.bat')
        bot.send_message(chat, "Yeniden Başlatıldı!")
        return
    os.startfile('basla.bat')
    bot.send_message(chat, "Bot Başlatıldı!")
    return

dpid = os.getpid()
eskipidfile = open("dpid.txt", "w+")
eskipidfile.write(str(dpid))
logs.info(dpid)

pid = os.getpid()
open("dpid.txt", "w").write(str(pid))
print(pid)

@bot.message_handler(commands=['stop'])
def stop(message):
    chat = message.chat.id
    user = message.from_user.id
    if not user in yetkili:
        bot.send_message(chat, "Bunu yapmak için yetkili değilsiniz!")
        return
    pidd = open("pid.txt", "r+")
    pid = pidd.read()
    if pid == "down":
        bot.send_message(chat, "Bot zaten kapalı")
        return
    try:
        os.kill(int(pid), 9)
    except Exception as e:
        print(e)
    pidd.write("down")
    bot.send_message(chat, "Bot Durduruldu.")

if __name__ == '__main__':
    threading.Thread(target=kontrol).start()
    logs.info("Bot Çalışıyor...")
    bot.polling()