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
baslangic = time.time()
bzaman = datetime.datetime.now()

def is_running():
    anapid = open("pid.txt", "r+").read()
    for q in psutil.process_iter():
        if q.name().startswith('python'):
            if q.pid == int(anapid):
                suan = time.time()
                # Biraz Matematik
                saniye = int(suan - baslangic)
                dakika = int(saniye / 60 if saniye > 60 else 0)
                saniye = saniye - dakika * 60
                saat = int(dakika / 60 if dakika > 60 else 0)
                dakika = dakika - saat * 60
                gun = int(saat / 24 if saat > 24 else 0)
                saat = saat - gun
                sure = str(gun).zfill(2)+" Gün "+str(saat).zfill(2)+":"+str(dakika).zfill(2)+":"+str(saniye).zfill(2)
                logs.info(f"{sure} İşlem hâlâ çalışıyor.")
                return True, sure
    logs.warning("İşlem Bulunamadı.")
    sure = "0 Gün 00:00:00"
    return False, sure

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
    yes, sure = is_running()
    if yes:
        durum = "Aktif!"
        bot.send_message(chat, "Merhaba!\n\nDurum: {}\nÇalışma Süresi: <code>{}</code>".format(durum, sure)) 
    else:
        durum = "Kapalı!"
        bot.send_message(chat, "Merhaba!\n\nDurum: {}".format(durum))

@bot.message_handler(commands=['run'])
def run(message):
    global baslangic
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
        os.startfile('main.py')
        bot.send_message(chat, "Yeniden Başlatıldı!")
        return
    os.startfile('main.py')
    baslangic = time.time()
    bot.send_message(chat, "Bot Başlatıldı!")
    return

@bot.channel_post_handler(commands=['postsil'])
def hhhh(m):
    print(m.reply_to_message.date)

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
    bot.send_message(chat, "Bot Durduruldu.")

if __name__ == '__main__':
    threading.Thread(target=kontrol).start()
    logs.info("Bot Çalışıyor...")
    bot.polling()