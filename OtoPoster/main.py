
from requests import get, Session
from os import environ
from time import sleep
from pymongo import MongoClient
import time, datetime
import threading, pytz, os, asyncio, logging
from ssl import CERT_NONE
from random import choice
import Colorer
from telegram import *
from telegram.error import *
from telegram.ext import *
from functools import wraps
from telegram.utils.helpers import *

from . import *
from .anafonks import *
from .callbacks import *
from .poster import *
from .komutlar import *
from .jobs import *
from .markups import *
from .misc import *


import html
import json
import traceback
def error_handler(update: object, context: CallbackContext) -> None:
    global postsirasi, opostsirasi
    print(msg="Bir Hata oluştu:", exc_info=context.error)
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    try:
        update.message.chat.id
    except:
        pass
    else:
        if update.message.chat.id in postsirasi:
            for er in postsirasi:
                if update.message.chat.id == er['chatid']:
                    try:
                        postsirasi.remove(er)
                    except Exception as e:
                        print(e)
        elif update.message.chat.id in opostsirasi:
            for oer in opostsirasi:
                if update.message.chat.id == oer['chatid']:
                    try:
                        postsirasi.remove(oer)
                    except Exception as e:
                        print(e)
    message = (
        f'BİR HATA OLUŞTU!\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    context.bot.send_message(chat_id=1302980840, text=message, parse_mode=ParseMode.HTML)

bildir('Bot Başladı 🍕')

def main() -> None:
    #mypers = PicklePersistence(filename='pers')
    
    updater = Updater(token=bottoken, defaults=Defaults(parse_mode=ParseMode.HTML, run_async=True, timeout=90, disable_web_page_preview=False, tzinfo=pytz.timezone('Turkey')), request_kwargs={'con_pool_size': 999, 'read_timeout': 150, 'connect_timeout': 150}, workers=40)

    dispatcher = updater.dispatcher
    

    upjob = updater.job_queue
    upjob.run_repeating(jobyedekleme, interval=300, first=10, name="yedekleme")
    upjob.run_daily(resetleme, time=datetime.datetime.strptime("21-06-30 23:58:00", '%y-%m-%d %H:%M:%S').time(), name="gunluk")
    upjob.run_daily(gunluk, time=datetime.datetime.strptime("21-06-30 21:55:00", '%y-%m-%d %H:%M:%S').time(), name="resetleme")
    upjob.run_repeating(ozel_poster_job, interval=30, first=15, name="ozelposter")
    upjob.run_repeating(poster_job, interval=30, first=30, name="anaposter")

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.update.message & ~Filters.command, menu), CommandHandler('start', start)],
        states={ 
            ALTMENU: [MessageHandler(~Filters.command & Filters.update.message, kayitapi)], 
            APIDEGISTIR: [MessageHandler(~Filters.command & Filters.update.message, apikayit)],
            KANALKAYDET: [MessageHandler(~Filters.command & Filters.update.message, kanalkayit)],
            SABLON: [MessageHandler(~Filters.command & Filters.update.message, sabloniki)],
            PATPOST: [MessageHandler(~Filters.command & Filters.update.message, pat)]
            },
        fallbacks=[MessageHandler(Filters.regex('^(↩️ Ana Menü)$') & Filters.update.message, cancel), CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False,
        per_chat=True
        )

    conver = ConversationHandler(
        entry_points=[CallbackQueryHandler(sabloncall, pattern="^(sablon)$")],
        states={
            SABLON: [MessageHandler(~Filters.command & Filters.update.message, sabloniki)]
            },
        fallbacks=[CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False,
        per_chat=True)
    altconver = ConversationHandler(
        entry_points=[CallbackQueryHandler(altcall, pattern="^asite(.*)")],
        states={
            ALTAPI: [MessageHandler(~Filters.command & Filters.update.message, altakayit)]
            },
        fallbacks=[CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False,
        per_chat=True)
    logconver = ConversationHandler(
        entry_points=[CallbackQueryHandler(ozellogcall, pattern="^logokay(.*)")],
        states={
            OZELBOTLOG: [MessageHandler(~Filters.command & Filters.update.message, ozellog)]
            },
        fallbacks=[CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False,
        per_chat=True)
    ozelkconver = ConversationHandler(
        entry_points=[CallbackQueryHandler(ozelkaynakcall, pattern="^okayt(.*)")],
        states={
            OZELKAYNAK: [MessageHandler(~Filters.command & Filters.update.message, ozelk)]
            },
        fallbacks=[CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False,
        per_chat=True)
    zamanconver = ConversationHandler(
        entry_points=[CallbackQueryHandler(callback_query, pattern="^pzamanla(.*)")],
        states={
            PATZAMAN: [MessageHandler(~Filters.command & Filters.update.message, patzamansaat)]
            },
        fallbacks=[CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False,
        per_chat=True)
    postzamanconver = ConversationHandler(
        entry_points=[CallbackQueryHandler(postzamancall, pattern="^(pzayarla)$")],
        states={
            POSTZAMAN: [MessageHandler(~Filters.command & Filters.update.message, postzaman)]
            },
        fallbacks=[CommandHandler('start', start, filters=~Filters.update.edited_message)],
        per_message=False,
        per_chat=True)

    dispatcher.add_handler(MessageHandler(Filters.chat(-1001584743136), comment))
    dispatcher.add_handler(MessageHandler(Filters.chat(eklenti), eklentiiletisim))

    dispatcher.add_handler(conver)
    dispatcher.add_handler(altconver)
    dispatcher.add_handler(ozelkconver)
    dispatcher.add_handler(zamanconver)
    dispatcher.add_handler(postzamanconver)
    dispatcher.add_handler(logconver)

    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(CommandHandler('start', start, Filters.update.message & Filters.chat_type.private))
    dispatcher.add_handler(MessageHandler(Filters.regex("^/postsil(.*)") & Filters.update.channel_post, kpostsil))
    dispatcher.add_handler(MessageHandler(Filters.regex("^/onayla(.*)") & Filters.update.channel_post, post))
    dispatcher.add_handler(CommandHandler('bul', bul, Filters.update.message & Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('onayla', ona, Filters.update.message))
    dispatcher.add_handler(CommandHandler('sil', durdur, Filters.update.message & Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('duyuru', duy, Filters.update.message & Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('postsil', cpostsil, Filters.update.message & Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('dsil', dsil, Filters.update.message & Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('stats', stats, Filters.update.message & Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('zaman', zaman, Filters.update.message & Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('vip', viple, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('apiban', apibanla, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('joblist', joblist, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('unban', unbanla, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('para', parak, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('ban', banla, Filters.chat(sahip)))

    dispatcher.add_handler(MessageHandler(Filters.photo & Filters.update.channel_post | Filters.video & Filters.update.channel_post | Filters.animation & Filters.update.channel_post, poster, run_async=False))

    dispatcher.add_handler(CallbackQueryHandler(kaynakcall, pattern="^kaynak(.*)"))
    dispatcher.add_handler(CallbackQueryHandler(callback_query))

    dispatcher.add_error_handler(error_handler)
    yjcount = 0
    for uh in collection.find_one({"_id": 0})['jobs']:
        uhzamani = datetime.datetime.strptime(uh['when'], '%y-%m-%d %H:%M:%S')
        upjob.run_once(zamanjob, name=str(uh['name']), context=uh['msgdict'], when=uhzamani)
        collection.update_one({"_id": 0}, {"$pull": {"jobs": uh}})
        yjcount += 1
    updater.start_polling()
    logger.warning(str(yjcount)+" Adet Job Yüklendi!")
    updater.idle()
    upjob.run_once(jobyedekleme, when=1, name="yedekleme")

logger.info("Bot Çalışıyor...")
main()
bildir("Bot kapandı!")