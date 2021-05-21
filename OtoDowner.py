import telebot
import os, signal
import time
import asyncio
import aiogram

token = "***REMOVED-BOT-TOKEN***"


yetkili = [1613760981, 755051086, 1302980840]

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
dp = Bot(token=API_TOKEN)
bot = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    chat = message.chat.id
    pid = open("pid.txt", "r").read()
    if pid.isdigit():
        durum = "Aktif!"
    else:
        durum = "Kapalı!"
    bot.send_message(chat, "Merhaba!\n\nDurum: {}".format(durum))










"""ott = telebot.TeleBot(token, parse_mode='html')

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
    if pid.isdigit():
        try:
            islem = os.kill(int(pid), 9)
        except:
            pass
        await asyncio.sleep(1)
        os.system('python main.py')
        bot.send_message(chat, "Yeniden Başlatıldı!")
        return
    os.system('python main.py')
    bot.send_message(chat, "Bot Başlatıldı!")
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

if __name__ == "__main__":
    asyncio.run(bot.polling(none_stop=True))
    print("Çalışıyor")
    """