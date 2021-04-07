import telebot
from os import environ
from telebot import *
from telegram import *
from logging import basicConfig, getLogger, INFO

LOGS = getLogger(__name__)

LOGS.info("Bot Çalışıyor...")

API_KEY = environ['BOT_TOKEN']

basicConfig(format="%(asctime)s - @TRLinkShortener - %(levelname)s - %(message)s",
            level=INFO)

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'], content_types=["text"])
def start(s):
    chat = s.chat.id
    user = s.from_user.first_name
    bot.send_message(chat, f"_Merhaba_ *{user}*, _Bu bot ile grup veya kanalınızdaki gönderileri kolayca temizleyebilirsiniz._ \n\n*Botu kanalınıza yönetici olarak ekleyin ve /temizle yazın*", parse_mode=ParseMode.MARKDOWN)

@bot.message_handler(commands=['temizle'])
def temizle(m):
    global sayı
    mesajlar = []
    sayi = 0
    chat = m.chat.id
    try:
        msg = m.reply_to_message.message_id
    except:
        bot.send_message(chat, f"Lütfen bir mesajı yanıtlayın.")
    while 500 > len(mesajlar):
        msg += 1
        mesajlar.append(msg)
        print(mesajlar)
        try:
            bot.delete_message(chat, msg)
        except:
            pass
        else:
            sayi += 1
        
    bot.send_message(chat, f"{sayi} adet mesaj temizlendi.")

@bot.channel_post_handler(commands=['temizle'])
def temizlik(m):
    global sayı
    mesajlar = []
    sayi = 0
    chat = m.chat.id
    try:
        msg = m.reply_to_message.message_id
    except:
        bot.send_message(chat, f"Lütfen bir mesajı yanıtlayın.")
    while 500 > len(mesajlar):
        msg += 1
        mesajlar.append(msg)
        try:
            bot.delete_message(chat, msg)
        except:
            pass
        else:
            sayi += 1
        
    bot.send_message(chat, f"`{sayi}` *adet mesaj temizlendi.*", parse_mode=ParseMode.MARKDOWN)
    bot.send_message(-1001391561285, f"`{sayi}` *adet mesaj silindi.*\n\n *Kanal:* `{chat}`", parse_mode=ParseMode.MARKDOWN)


bot.polling()