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
    upjob.run_repeating(siraclean, interval=3600, first=10, name="yedekleme")
    """ Misc """
    dispatcher.add_handler(MessageHandler(Filters.chat(-1001584743136), comment))
    dispatcher.add_handler(MessageHandler(Filters.chat(eklenti), eklentiiletisim))
    dispatcher.add_handler(MessageHandler(Filters.chat(-1001572618573), posterkomut2)) 
    dispatcher.add_handler(MessageHandler(Filters.photo & Filters.update.edited_channel_post | Filters.video & Filters.update.edited_channel_post | Filters.animation & Filters.update.edited_channel_post, poster_edit))
    """ Admin Komutları """
    dispatcher.add_handler(AdminCommandHandler('bul', bul))
    dispatcher.add_handler(AdminCommandHandler('duyuru', duy))
    dispatcher.add_handler(AdminCommandHandler('dsil', dsil))
    dispatcher.add_handler(AdminCommandHandler('stats', stats))
    dispatcher.add_handler(AdminCommandHandler('vip', viple))
    dispatcher.add_handler(AdminCommandHandler('duraklat', duraklat))
    dispatcher.add_handler(AdminCommandHandler('apiban', apibanla))
    dispatcher.add_handler(AdminCommandHandler('cekilis', cekilis))
    dispatcher.add_handler(AdminCommandHandler('sonuc', sonuclandir))
    dispatcher.add_handler(AdminCommandHandler('joblist', joblist))
    dispatcher.add_handler(AdminCommandHandler('sira', postersira))
    dispatcher.add_handler(AdminCommandHandler('postsil', cpostsil))
    dispatcher.add_handler(AdminCommandHandler('set', SetKomutu))
    dispatcher.add_handler(AdminCommandHandler('exec', exece))
    dispatcher.add_handler(AdminCommandHandler('eval', evale))
    dispatcher.add_handler(AdminCommandHandler('poster', posterkomut))
    dispatcher.add_handler(AdminCommandHandler('unban', unbanla))
    dispatcher.add_handler(AdminCommandHandler('loot', Loot))
    dispatcher.add_handler(AdminCommandHandler('kaynak', yenikaynakkomutu))
    dispatcher.add_handler(AdminCommandHandler('para', parak))
    dispatcher.add_handler(AdminCommandHandler('ban', banla))
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
            TSPOST: [MessageHandler(~Filters.command, tekrarlipostayarla), CallbackQueryHandler(tsmodcall, pattern="^(tsmod-rastgele|tsmod-sirali)$")],
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
    dispatcher.add_handler(MessageHandler(Filters.regex("^(/sil)$") & Filters.update.channel_post, KanalSilKomutu))
    dispatcher.add_handler(CommandHandler('onayla', ona, Filters.update.message))
    dispatcher.add_handler(CommandHandler('sil', durdur, Filters.update.message & Filters.chat_type.private))
    """ Kaynak Komutları """
    dispatcher.add_handler(MessageHandler(Filters.regex("^/postsil(.*)") & Filters.update.channel_post, kpostsil))
    dispatcher.add_handler(CommandHandler('iptal', IptalPoster))
    dispatcher.add_handler(CommandHandler('zaman', zaman, Filters.update.message & Filters.chat_type.private))
    """ Poster """
    dispatcher.add_handler(MessageHandler(Filters.photo & Filters.update.channel_post | Filters.video & Filters.update.channel_post | Filters.animation & Filters.update.channel_post, poster, run_async=False))
    """ Callbacks """
    dispatcher.add_handler(CallbackQueryHandler(panelcall, pattern="^(pau(.*)|pak(.*)|pan(.*))", run_async=False))
    dispatcher.add_handler(CallbackQueryHandler(cekiliscall, pattern="^katil(.*)"))
    dispatcher.add_handler(CallbackQueryHandler(kaynakcall, pattern="^kaynak(.*)"))
    dispatcher.add_handler(CallbackQueryHandler(begeniislemcall, pattern="^begeni-(.*)", run_async=False))
    dispatcher.add_handler(CallbackQueryHandler(advcall, pattern="^adv(.*)"))
    dispatcher.add_handler(CallbackQueryHandler(callback_query))
    """ Error Handler """
    dispatcher.add_error_handler(error_handler)
    """ Job Yedekleme """
    yjcount = 0
    ytjcount = 0
    for uh in collection.find_one({"_id": 0})['jobs']:
        if uh['name'].startswith("ts"):
            firtime = datetime.datetime.strptime(uh['msgdict']["tetik"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.timezone('Europe/Istanbul'))
            print(type(firtime))
            vakit = datetime.datetime.now(pytz.timezone('Europe/Istanbul'))
            print(type(vakit))
            firt = firtime - vakit
            upjob.run_repeating(tekrarlipostjob, first=firt.total_seconds(), interval=3600*int(uh['msgdict']['tsaat']), name=uh['name'], context=uh['msgdict'])
            ytjcount += 1
            continue
        yjcount += 1
        uhzamani = datetime.datetime.strptime(uh['when'], '%y-%m-%d %H:%M:%S')
        upjob.run_once(zamanjob, name=str(uh['name']), context=uh['msgdict'], when=uhzamani)
    logger.warning(str(yjcount)+" Adet Tekil, "+str(ytjcount)+" Adet Tekrarlı Job Yüklendi!")
    """ Polling """
    komutisimleristart()
    updater.start_polling()
    updater.idle()


    upjob.run_once(jobyedekleme, when=1, name="yedekleme")

logger.info("Bot Çalışıyor...")
main()
bildir("Bot kapandı!")