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
    """ Misc """
    dispatcher.add_handler(MessageHandler(Filters.chat(-1001584743136), comment))
    dispatcher.add_handler(MessageHandler(Filters.chat(eklenti), eklentiiletisim))
    dispatcher.add_handler(MessageHandler(Filters.chat(-1001572618573), posterkomut2)) 
    dispatcher.add_handler(MessageHandler(Filters.photo & Filters.update.edited_channel_post | Filters.video & Filters.update.edited_channel_post | Filters.animation & Filters.update.edited_channel_post, poster_edit))
    """ Admin Komutları """
    dispatcher.add_handler(CommandHandler('bul', bul, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('duyuru', duy, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('dsil', dsil, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('stats', stats, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('vip', viple, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('duraklat', duraklat, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('apiban', apibanla, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('cekilis', cekilis, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('sonuc', sonuclandir, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('joblist', joblist, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('sira', postersira, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('postsil', cpostsil, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('set', SetKomutu, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('poster', posterkomut, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('unban', unbanla, Filters.chat(sahip)))
    dispatcher.add_handler(CommandHandler('para', parak, Filters.chat(sahip)))
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
        CallbackQueryHandler(callback_query, pattern="^pzamanla(.*)"),
        CallbackQueryHandler(devampatcall, pattern="^devam(.*)"),
        CallbackQueryHandler(begenicall, pattern="^begeniolustur(.*)"),
        CallbackQueryHandler(tekrarlisaatayarlacall, pattern="^ts-(.*)"),
        CallbackQueryHandler(panelcall, pattern="^(panelzaman|pau-bul|pak-bul)$")
        ],
        states={ 
            KANALMENU: [MessageHandler(~Filters.command & Filters.update.message, kanalmenu), 
            CallbackQueryHandler(panelcall, pattern="^(panelzaman|pau-bul|pak-bul)$")],
            APIMENU: [MessageHandler(~Filters.command & Filters.update.message, apimenu),  
            CallbackQueryHandler(altcall, pattern="^asite(.*)"),
            CallbackQueryHandler(panelcall, pattern="^(panelzaman|pau-bul|pak-bul)$")],
            POSTMENU: [MessageHandler(~Filters.command & Filters.update.message, postmenu),
            CallbackQueryHandler(sabloncall, pattern="^(sablon)$"),
            CallbackQueryHandler(panelcall, pattern="^(panelzaman|pau-bul|pak-bul)$"),
            CallbackQueryHandler(ozelkaynakcall, pattern="^okayt(.*)"),
            CallbackQueryHandler(ozellogcall, pattern="^logokay(.*)"), 
            CallbackQueryHandler(postzamancall, pattern="^(pzayarla)$"),
            CallbackQueryHandler(callback_query, pattern="^pzamanla(.*)")], 
            EKSTRAMENU: [MessageHandler(~Filters.command & Filters.update.message, ekstramenu),
            CallbackQueryHandler(begenicall, pattern="^(begeniolustur)$"),
            CallbackQueryHandler(panelcall, pattern="^(panelzaman|pau-bul|pak-bul)$"),
            CallbackQueryHandler(tekrarlisaatayarlacall, pattern="^ts-(.*)")],
            TSPOST: [MessageHandler(~Filters.command, tekrarlipostayarla)],
            PANELZAMAN: [MessageHandler(~Filters.command & Filters.text, zaman)],
            PANELBUL: [MessageHandler(~Filters.command & Filters.forwarded | Filters.text & ~Filters.command, panelbul)],
            TSBASLIK: [MessageHandler(~Filters.command & Filters.text, tekrarlipostbaslikayarla)],
            BEGENI: [MessageHandler(~Filters.command & Filters.text, begenidegistir)],
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
    dispatcher.add_handler(CommandHandler('panel', kaynakpanel))
    dispatcher.add_handler(CommandHandler('start', start, Filters.update.message & Filters.chat_type.private))
    dispatcher.add_handler(MessageHandler(Filters.regex("^/onayla(.*)") & Filters.update.channel_post, post))
    dispatcher.add_handler(CommandHandler('onayla', ona, Filters.update.message))
    dispatcher.add_handler(CommandHandler('sil', durdur, Filters.update.message & Filters.chat_type.private))
    """ Kaynak Komutları """
    dispatcher.add_handler(MessageHandler(Filters.regex("^/postsil(.*)") & Filters.update.channel_post, kpostsil))
    dispatcher.add_handler(CommandHandler('iptal', IptalPoster))
    dispatcher.add_handler(CommandHandler('zaman', zaman, Filters.update.message & Filters.chat_type.private))
    """ Poster """
    dispatcher.add_handler(MessageHandler(Filters.photo & Filters.update.channel_post | Filters.video & Filters.update.channel_post | Filters.animation & Filters.update.channel_post, poster, run_async=False))
    """ Callbacks """
    dispatcher.add_handler(CallbackQueryHandler(panelcall, pattern="^(pau(.*)|pak(.*)|pan(.*))"))
    dispatcher.add_handler(CallbackQueryHandler(cekiliscall, pattern="^katil(.*)"))
    dispatcher.add_handler(CallbackQueryHandler(kaynakcall, pattern="^kaynak(.*)"))
    dispatcher.add_handler(CallbackQueryHandler(begeniislemcall, pattern="^begeni-(.*)", run_async=False))
    dispatcher.add_handler(CallbackQueryHandler(callback_query))
    """ Error Handler """
    dispatcher.add_error_handler(error_handler)
    """ Job Yedekleme """
    yjcount = 0
    ytjcount = 0
    for uh in collection.find_one({"_id": 0})['jobs']:
        if uh['name'].startswith("ts"):
            upjob.run_repeating(tekrarlipostjob, interval=3600*int(uh['msgdict']['tsaat']), name=uh['name'], context=uh['msgdict'])
            ytjcount += 1
            continue
        yjcount += 1
        uhzamani = datetime.datetime.strptime(uh['when'], '%y-%m-%d %H:%M:%S')
        upjob.run_once(zamanjob, name=str(uh['name']), context=uh['msgdict'], when=uhzamani)
    logger.warning(str(yjcount)+" Adet Job Yüklendi!")
    """ Polling """
    updater.start_polling()
    updater.idle()


    upjob.run_once(jobyedekleme, when=1, name="yedekleme")

logger.info("Bot Çalışıyor...")
try:
    main()
except:
    pass
bildir("Bot kapandı!")