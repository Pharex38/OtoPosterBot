import telebot
import os, signal
import time
import asyncio
import aiogram
import logging
import subprocess
from aiogram import Bot, Dispatcher, executor, types
import Colorer
import psutil
import time, datetime

token = "***REMOVED-BOT-TOKEN***"

yetkili = [1613760981, 755051086, 1302980840]

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",level=logging.INFO)
logs = logging.getLogger(__name__)

dp = Bot(token=token)
bot = Dispatcher(dp)
def is_running():
    anapid = open("pid.txt", "r+").read()
    for q in psutil.process_iter():
        if q.name().startswith('python'):
            if q.pid == int(anapid):
                logs.info("İşlem hâlâ çalışıyor.")
                return True
    logs.warning("İşlem Bulunamadı.")
    return False

async def kontrol()
    while True:
        if not is_running():
            dp.send_message(1302980840, "Bot çöktü!")
            break
        else:
            time.sleep(60)

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
logs.info("Eski İşlem Kapatıldı")

@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    chat = message.chat.id
    pid = open("pid.txt", "r").read()
    if is_running():
        durum = "Aktif!"
    else:
        durum = "Kapalı!"
    await dp.send_message(chat, "Merhaba!\n\nDurum: {}".format(durum))

@bot.message_handler(commands=['run'])
async def run(message: types.Message):
    chat = message.chat.id
    user = message.from_user.id
    if not user in yetkili:
        await dp.send_message(chat, "Bunu yapmak için yetkili değilsiniz!")
        return
    pidd = open("pid.txt", "r+")
    pid = pidd.read()
    if pid.isdigit():
        try:
            islem = os.kill(int(pid), 9)
        except:
            pass
        await asyncio.sleep(1)
        os.startfile('basla.bat')
        await dp.send_message(chat, "Yeniden Başlatıldı!")
        return
    os.startfile('basla.bat')
    await dp.send_message(chat, "Bot Başlatıldı!")
    return


dpid = os.getpid()
eskipidfile = open("dpid.txt", "w+")
eskipidfile.write(str(dpid))
logs.info(dpid)


pid = os.getpid()
open("dpid.txt", "w").write(str(pid))
print(pid)

@bot.message_handler(commands=['stop'])
async def stop(message: types.Message):
    chat = message.chat.id
    user = message.from_user.id
    if not user in yetkili:
        await dp.send_message(chat, "Bunu yapmak için yetkili değilsiniz!")
        return
    pidd = open("pid.txt", "r+")
    pid = pidd.read()
    if pid == "down":
        await dp.send_message(chat, "Bot zaten kapalı")
        return
    try:
        await os.kill(int(pid), 9)
    except Exception as e:
        print(e)
    pidd.write("down")
    await dp.send_message(chat, "Bot Durduruldu.")




if __name__ == '__main__':
    executor.start_polling(bot, skip_updates=True)
    logs.info("Bot Çalışıyor...")