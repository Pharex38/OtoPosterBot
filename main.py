import telebot
from os import environ
from telegram import *

API_KEY = environ['BOT_TOKEN']

bot = telebot.TeleBot(API_KEY)

print("Çalışıyor...")

class Kayit:
    def __init__(self):
        self.papara = None
        self.id = None
        self.kadi = None
    

@bot.message_handler(commands=['start'])
def start(s):
    chat = s.chat.id
    mesaj = bot.send_message(chat, "Kullanıcının Papara numarası nedir?")
    bot.register_next_step_handler(mesaj, idfonk)

def idfonk(i):
    chat = i.chat.id
    papara = i.text
    if not papara.isdigit() or len(papara) < 10 or len(papara) > 10:
        mesaj = bot.send_message(chat, "Lütfen geçerli bir Papara numarası gönder.")
        bot.register_next_step_handler(mesaj, idfonk)
        return 
    mesaj = bot.send_message(chat, "Kullanıcının ID'si nedir?")
    Kayit.papara = papara
    bot.register_next_step_handler(mesaj, isim)
    
def isim(a):
    chat = a.chat.id
    id = a.text
    if not id.isdigit() or len(id) < 9 or len(id) > 11:
        mesaj = bot.send_message(chat, "Lütfen geçerli bir ID gönder.")
        bot.register_next_step_handler(mesaj, isim)
        return
    mesaj = bot.send_message(chat, "Kullanıcı adı nedir?")
    Kayit.id = id
    bot.register_next_step_handler(mesaj, son)

def son(b):
    chat = b.chat.id
    isim = b.text
    link = bot.createChatInviteLink(-1254179689, member_limit=1)
    if not isim.startswith("@"):
        bot.send_message(chat, f"Tamamdır Link: {link}")
        Kayit.kadi = isim
        user_id = Kayit.id
        bot.send_message(-1001476303153, f"Papara: {Kayit.papara}\nKullanıcı Adı: @{Kayit.kadi}\nID: {Kayit.id}\n\n [Kalici Link](tg://user?id={user_id})", parse_mode=ParseMode.MARKDOWN)
    else:
        bot.send_message(chat, f"Tamamdır Link: {link}")
        Kayit.kadi = isim
        user_id = Kayit.id
        bot.send_message(-1001476303153, f"Papara: {Kayit.papara}\nKullanıcı Adı: {Kayit.kadi}\nID: {Kayit.id}\n\n [Kalici Link](tg://user?id={user_id})", parse_mode=ParseMode.MARKDOWN)


bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling()