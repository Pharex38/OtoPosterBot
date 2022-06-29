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
    global application, persistence, upjob, cjrhandler

    persistence = PicklePersistence(filename='OtoPosterPersistence', store_user_data=True, store_chat_data=True, single_file=True, store_callback_data=True)
    application = Application.builder().bot(bot).persistence(persistence)
    upjob = application.job_queue
    """ Repeating Jobs """
    upjob.run_daily(gunluk, time=datetime.datetime.strptime("21-06-30 21:55:00", '%y-%m-%d %H:%M:%S').time(), name="resetleme")
    upjob.run_repeating(jobyedekleme, interval=300, first=10, name="yedekleme")
    upjob.run_repeating(siraclean, interval=3600, first=10, name="yedekleme")
    """ Misc """
    application.add_handler(MessageHandler(filters.chat(-1001584743136), comment))
    application.add_handler(MessageHandler(filters.chat(eklenti), eklentiiletisim))
    application.add_handler(MessageHandler(filters.chat(-1001572618573), posterkomut2)) 
    #application.add_handler(MessageHandler(filters.photo & filters.update.edited_channel_post | filters.video & filters.update.edited_channel_post | filters.animation & filters.update.edited_channel_post, poster_edit))
    """ Admin Komutları """
    application.add_handler(AdminCommandHandler('bul', bul))
    application.add_handler(AdminCommandHandler('duyuru', duy))
    application.add_handler(AdminCommandHandler('dsil', dsil))
    application.add_handler(AdminCommandHandler('stats', stats))
    application.add_handler(AdminCommandHandler('vip', viple))
    application.add_handler(AdminCommandHandler('duraklat', duraklat))
    application.add_handler(AdminCommandHandler('apiban', apibanla))
    application.add_handler(AdminCommandHandler('cekilis', cekilis))
    application.add_handler(AdminCommandHandler('sonuc', sonuclandir))
    application.add_handler(AdminCommandHandler('joblist', joblist))
    application.add_handler(AdminCommandHandler('sira', postersira))
    application.add_handler(AdminCommandHandler('postsil', cpostsil))
    application.add_handler(AdminCommandHandler('set', SetKomutu))
    application.add_handler(AdminCommandHandler('exec', exece))
    application.add_handler(AdminCommandHandler('eval', evale))
    application.add_handler(AdminCommandHandler('poster', posterkomut))
    application.add_handler(AdminCommandHandler('unban', unbanla))
    application.add_handler(AdminCommandHandler('loot', Loot))
    application.add_handler(AdminCommandHandler('kaynak', yenikaynakkomutu))
    application.add_handler(AdminCommandHandler('para', parak))
    application.add_handler(AdminCommandHandler('ayarlar', AyarlarKomutu))
    application.add_handler(AdminCommandHandler('ban', banla))
    """ Menü """
    conv_handler = ConversationHandler(
        entry_points=[
        MessageHandler(filters.update.message & ~filters.command & filters.chat_type.private, menu), 
        CommandHandler('start', start, filters.chat_type.private),
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
            KANALMENU: [MessageHandler(~filters.command & filters.update.message, kanalmenu), 
            CallbackQueryHandler(panelcall, pattern="^(panelzaman|pau-bul|pak-bul)$")],
            APIMENU: [MessageHandler(~filters.command & filters.update.message, apimenu),  
            CallbackQueryHandler(altcall, pattern="^asite(.*)"),
            CallbackQueryHandler(panelcall, pattern="^(panelzaman|pau-bul|pak-bul)$")],
            POSTMENU: [MessageHandler(~filters.command & filters.update.message, postmenu),
            CallbackQueryHandler(sabloncall, pattern="^(sablon)$"),
            CallbackQueryHandler(panelcall, pattern="^(panelzaman|pau-bul|pak-bul)$"),
            CallbackQueryHandler(ozelkaynakcall, pattern="^okayt(.*)"),
            CallbackQueryHandler(ozellogcall, pattern="^logokay(.*)"), 
            CallbackQueryHandler(postzamancall, pattern="^(pzayarla)$"),
            CallbackQueryHandler(callback_query, pattern="^pzamanla(.*)")], 
            EKSTRAMENU: [MessageHandler(~filters.command & filters.update.message, ekstramenu),
            CallbackQueryHandler(begenicall, pattern="^(begeniolustur)$"),
            CallbackQueryHandler(panelcall, pattern="^(panelzaman|pau-bul|pak-bul)$"),
            CallbackQueryHandler(tekrarlisaatayarlacall, pattern="^ts-(.*)")],
            TSPOST: [MessageHandler(~filters.command, tekrarlipostayarla), CallbackQueryHandler(tsmodcall, pattern="^(tsmod-rastgele|tsmod-sirali)$")],
            PANELZAMAN: [MessageHandler(~filters.command & filters.text, zaman)],
            PANELBUL: [MessageHandler(~filters.command & filters.forwarded | filters.text & ~filters.command, panelbul)],
            TSBASLIK: [MessageHandler(~filters.command & filters.text, tekrarlipostbaslikayarla)],
            BEGENI: [MessageHandler(~filters.command & filters.text, begenidegistir)],
            APIDEGISTIR: [MessageHandler(~filters.command & filters.update.message, apikayit)],
            KANALKAYDET: [MessageHandler(~filters.command & filters.update.message, kanalkayit)],
            SABLONA: [MessageHandler(~filters.command & filters.update.message, sabloniki)],
            PATPOST: [MessageHandler(~filters.command & filters.update.message, pat)],
            PATZAMAN: [MessageHandler(~filters.command & filters.update.message, patzamansaat)],
            ALTAPI: [MessageHandler(~filters.command & filters.update.message, altakayit)],
            OZELBOTLOG: [MessageHandler(~filters.command & filters.update.message, ozellog)],
            OZELKAYNAK: [MessageHandler(~filters.command & filters.update.message, ozelk)],
            POSTZAMAN: [MessageHandler(~filters.command & filters.update.message, postzaman)]
            },
        fallbacks=[MessageHandler(filters.regex('^(↩️ Ana Menü)$') & filters.update.message, cancel), CommandHandler('start', start, filters=~filters.update.edited_message)],
        per_message=False,
        name="anaconv",
        per_chat=True
        )
    application.add_handler(conv_handler)
    """ Müşteri Komutları """
    application.add_handler(CommandHandler('panel', kaynakpanel))
    #application.add_handler(CommandHandler('kaynak', kaynakkontrol))
    application.add_handler(CommandHandler('start', start, filters.update.message & filters.chat_type.private))
    application.add_handler(MessageHandler(filters.regex("^/onayla(.*)") & filters.update.channel_post, post))
    application.add_handler(MessageHandler(filters.regex("^(/sil)$") & filters.update.channel_post, KanalSilKomutu))
    application.add_handler(CommandHandler('onayla', ona, filters.update.message))
    application.add_handler(CommandHandler('sil', durdur, filters.update.message & filters.chat_type.private))
    """ Kaynak Komutları """
    application.add_handler(MessageHandler(filters.regex("^/postsil(.*)") & filters.update.channel_post, kpostsil))
    application.add_handler(CommandHandler('iptal', IptalPoster))
    application.add_handler(CommandHandler('zaman', zaman, filters.update.message & filters.chat_type.private))
    """ Poster """
    application.add_handler(MessageHandler(filters.photo & filters.update.channel_post | filters.video & filters.update.channel_post | filters.animation & filters.update.channel_post, poster))
    """ Callbacks """
    application.add_handler(CallbackQueryHandler(panelcall, pattern="^(pau(.*)|pak(.*)|pan(.*))"))
    application.add_handler(CallbackQueryHandler(cekiliscall, pattern="^katil(.*)"))
    application.add_handler(CallbackQueryHandler(kaynakkontrolcall, pattern="^kont(.*)"))
    application.add_handler(CallbackQueryHandler(kaynakcall, pattern="^kaynak(.*)"))
    application.add_handler(CallbackQueryHandler(begeniislemcall, pattern="^begeni-(.*)"))
    application.add_handler(CallbackQueryHandler(advcall, pattern="^adv(.*)"))
    application.add_handler(CallbackQueryHandler(callback_query))
    """ Error Handler """
    application.add_error_handler(error_handler)
    """ Job Yedekleme """
    yjcount = 0
    ytjcount = 0
    for uh in collection.find_one({"_id": 0})['jobs']:
        if uh['name'].startswith("ts"):
            if uh['msgdict'].get("tetik", None) == None:
                continue
            firtime = datetime.datetime.strptime(uh['msgdict']["tetik"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.timezone('Europe/Istanbul'))
            vakit = datetime.datetime.now(pytz.timezone('Europe/Istanbul'))
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
    application.start_polling()



    upjob.run_once(jobyedekleme, when=1, name="yedekleme")

logger.info("Bot Çalışıyor...")
main()
bildir("Bot kapandı!")
