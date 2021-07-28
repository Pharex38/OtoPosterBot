
from requests import get, Session
from os import environ
from time import sleep
from pymongo import MongoClient
import time, datetime
import threading, pytz, os, asyncio
from ssl import CERT_NONE
from random import choice
from telegram import *
from telegram.error import *
from telegram.ext import *
from functools import wraps
from telegram.utils.helpers import *
import html
import json as jason
import traceback
from telegram.utils.request import Request
from . import *
from .anafonks import *
from .callbacks import *
from .poster import *
from .komutlar import *
from .jobs import *
from .markups import *
from .misc import *



bildir('Bot Başladı 🍕')

def main() -> None:

    persistence = PicklePersistence(filename='OtoPosterPersistence', store_user_data=True, store_chat_data=True, single_file=True, store_callback_data=True)
    updater = Updater(bot=bot, workers=40, persistence=persistence)
    dispatcher = updater.dispatcher
    upjob = updater.job_queue

    """ Repeating Jobs """
    upjob.run_daily(resetleme, time=datetime.datetime.strptime("21-06-30 23:58:00", '%y-%m-%d %H:%M:%S').time(), name="gunluk")
    upjob.run_daily(gunluk, time=datetime.datetime.strptime("21-06-30 21:55:00", '%y-%m-%d %H:%M:%S').time(), name="resetleme")
    upjob.run_repeating(jobyedekleme, interval=300, first=10, name="yedekleme")
    upjob.run_repeating(postsiralandirici, interval=20, first=3, name="ozelpostersiralayici")
    #upjob.run_repeating(opostsiralandirici, interval=30, first=30, name="anapostersiralayici")
    """ Misc """
    dispatcher.add_handler(MessageHandler(Filters.chat(-1001584743136), comment))
    dispatcher.add_handler(MessageHandler(Filters.chat(eklenti), eklentiiletisim))
    dispatcher.add_handler(MessageHandler(Filters.chat(-1001572618573), posterkomut2)) 
    dispatcher.add_handler(MessageHandler(Filters.update.edited_channel_post, poster_edit))
    """ Admin Komutları """
    dispatcher.add_handler(CommandHandler('bul', bul, Filters.update.message & Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('duyuru', duy, Filters.update.message & Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('dsil', dsil, Filters.update.message & Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('stats', stats, Filters.update.message & Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('vip', viple, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('apiban', apibanla, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('joblist', joblist, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('unban', unbanla, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('para', parak, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('poster', posterkomut, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('ban', banla, Filters.chat(sahip)))
    """ Menü """
    conv_handler = ConversationHandler(
        entry_points=[
        MessageHandler(Filters.update.message & ~Filters.command & Filters.chat_type.private, menu), 
        CommandHandler('start', start, Filters.chat_type.private),
        CallbackQueryHandler(sabloncall, pattern="^(sablon)$"),
        CallbackQueryHandler(ozelkaynakcall, pattern="^okayt(.*)"),
        CallbackQueryHandler(ozellogcall, pattern="^logokay(.*)"),
        CallbackQueryHandler(altcall, pattern="^asite(.*)"),
        CallbackQueryHandler(postzamancall, pattern="^(pzayarla)$"),
        CallbackQueryHandler(callback_query, pattern="^pzamanla(.*)")
        ],
        states={ 
            KANALMENU: [MessageHandler(~Filters.command & Filters.update.message, kanalmenu)],
            APIMENU: [MessageHandler(~Filters.command & Filters.update.message, apimenu),  
            CallbackQueryHandler(altcall, pattern="^asite(.*)")],
            POSTMENU: [MessageHandler(~Filters.command & Filters.update.message, postmenu),
            CallbackQueryHandler(sabloncall, pattern="^(sablon)$"),
            CallbackQueryHandler(ozelkaynakcall, pattern="^okayt(.*)"),
            CallbackQueryHandler(ozellogcall, pattern="^logokay(.*)"), 
            CallbackQueryHandler(postzamancall, pattern="^(pzayarla)$"),
            CallbackQueryHandler(callback_query, pattern="^pzamanla(.*)")], 
            APIDEGISTIR: [MessageHandler(~Filters.command & Filters.update.message, apikayit)],
            KANALKAYDET: [MessageHandler(~Filters.command & Filters.update.message, kanalkayit)],
            SABLONA: [MessageHandler(~Filters.command & Filters.update.message, sabloniki)],
            PATPOST: [MessageHandler(~Filters.command & Filters.update.message, pat)],
            PATZAMAN: [MessageHandler(~Filters.command & Filters.update.message, patzamansaat)],
            ALTAPI: [MessageHandler(~Filters.command & Filters.update.message, altakayit)],
            OZELBOTLOG: [MessageHandler(~Filters.command & Filters.update.message, ozellog)],
            OZELKAYNAK: [MessageHandler(~Filters.command & Filters.update.message, ozelk)],
            POSTZAMAN: [MessageHandler(~Filters.command & Filters.update.message, postzaman)]
            },
        fallbacks=[MessageHandler(Filters.regex('^(↩️ Ana Menü)$') & Filters.update.message, cancel), CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False,
        name="anaconv",
        per_chat=True
        )
    dispatcher.add_handler(conv_handler)
    """ Müşteri Komutları """
    dispatcher.add_handler(CommandHandler('start', start, Filters.update.message & Filters.chat_type.private))
    dispatcher.add_handler(MessageHandler(Filters.regex("^/onayla(.*)") & Filters.update.channel_post, post))
    dispatcher.add_handler(CommandHandler('onayla', ona, Filters.update.message))
    dispatcher.add_handler(CommandHandler('sil', durdur, Filters.update.message & Filters.chat_type.private))
    """ Kaynak Komutları """
    dispatcher.add_handler(MessageHandler(Filters.regex("^/postsil(.*)") & Filters.update.channel_post, kpostsil))
    dispatcher.add_handler(CommandHandler('iptal', IptalPoster))
    dispatcher.add_handler(CommandHandler('zaman', zaman, Filters.update.message & Filters.chat_type.private))
    """ Poster """
    dispatcher.add_handler(MessageHandler(Filters.photo & Filters.update.channel_post | Filters.video & Filters.update.channel_post | Filters.animation & Filters.update.channel_post, poster, run_async=True))
    """ Callbacks """
    dispatcher.add_handler(CallbackQueryHandler(kaynakcall, pattern="^kaynak(.*)"))
    dispatcher.add_handler(CallbackQueryHandler(callback_query))
    """ Error Handler """
    dispatcher.add_error_handler(error_handler)
    """ Job Yedekleme """
    yjcount = 0
    for uh in collection.find_one({"_id": 0})['jobs']:
        uhzamani = datetime.datetime.strptime(uh['when'], '%y-%m-%d %H:%M:%S')
        upjob.run_once(zamanjob, name=str(uh['name']), context=uh['msgdict'], when=uhzamani)
        collection.update_one({"_id": 0}, {"$pull": {"jobs": uh}})
        yjcount += 1
    logger.warning(str(yjcount)+" Adet Job Yüklendi!")
    """ Polling """
    updater.start_polling()
    updater.idle()

    upjob.run_once(jobyedekleme, when=1, name="yedekleme")

logger.info("Bot Çalışıyor...")
main()
bildir("Bot kapandı!")