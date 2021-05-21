import telebot
import os, signal
import time
import asyncio

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
async def run(m):
    chat = await m.chat.id
    user = await m.from_user.id
    if not user in yetkili:
        await bot.send_message(chat, "Bunu yapmak için yetkili değilsiniz!")
        return
    pidd = await open("pid.txt", "r+")
    pid = await pidd.read()
    await if pid.isdigit():
        await try:
            islem = await os.kill(int(pid), 9)
        await except:
            pass
        await asyncio.sleep(1)
        await bot.send_message(chat, "Yeniden Başlatıldı!")
        os.system('python main.py')
        return
    os.system('python main.py')
    await bot.send_message(chat, "Bot Başlatıldı!")
    return

@bot.message_handler(commands=['stop'])
def stop(p):
    chat = p.chat.id
    user = p.from_user.id
    if not user in yetkili:
        bot.send_message(chat, "Bunu yapmak için yetkili değilsiniz!")
        return
    pidd = open("pid.txt", "r+")
    pid = pidd.read()
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