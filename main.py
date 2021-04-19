import telebot
import environ
from os import environ

bot = telebot.TeleBot(environ['BOT_TOKEN'])

print("Çalışıyor...")

@bot.message_handler(commands=['start'])
def start(s):
    chat = s.chat.id
    mesaj = bot.send_message(chat, "Kullanıcının Papara numarası nedir?")
    papara = s.text
    bot.register_next_step_handler(mesaj, idfonk)

def idfonk(i):
    chat = i.chat.id
    mesaj = bot.send_message(chat, "Kullanıcının ID'si nedir?")
    id = i.text
    bot.register_next_step_handler(mesaj, isim)
    
def isim(a):
    chat = a.chat.id
    mesaj = bot.send_message(chat, "Kullanıcının ismi nedir?")
    isim = a.text
    
bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling()