import telebot
from os import environ

API_KEY = environ['BOT_TOKEN']

bot = telebot.TeleBot(API_KEY)

print("Çalışıyor...")

user_dict = {}

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
    mesaj = bot.send_message(chat, "Kullanıcının ID'si nedir?")
    papara = i.text
    print(papara)
    Kayit.papara = papara
    bot.register_next_step_handler(mesaj, isim)
    
def isim(a):
    chat = a.chat.id
    mesaj = bot.send_message(chat, "Kullanıcının ismi nedir?")
    id = a.text
    print(id)
    Kayit.id = id
    bot.register_next_step_handler(mesaj, son)

def son(b):
    chat = b.chat.id
    mesaj = bot.send_message(chat, "Tamamdır")
    isim = b.text
    print(isim)
    Kayit.kadi = isim
    print(Kayit.id, Kayit.papara)
    print(user_dict)
    bot.send_message(-1001292327505,
    user_id = message.from_user.id
    
    f"Papara: {Kayit.papara}\nKullanıcı Adı: {Kayit.kadi}\nID: {Kayit.id}\n\n [Kalici Link](tg://user?id={user_id})", parse_mode=ParseMode.MARKDOWN)
    
bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling()