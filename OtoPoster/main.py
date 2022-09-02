from . import *
from .anafonks import *
from .callbacks import *
from .poster import *
from .komutlar import *
from .jobs import *
from .markups import *
from .misc import *




def main() -> None:
    global application, persistence, upjob, bot

    persistence = PicklePersistence(filepath='OtoPosterPersistence', single_file=True)
    builder = Application.builder()
    builder.token(bottoken)
    builder.defaults(Defaults(parse_mode=ParseMode.HTML, block=False, disable_web_page_preview=True, allow_sending_without_reply=True, tzinfo=pytz.timezone('Turkey')))
    builder.persistence(persistence)
    builder.connection_pool_size(50000)
    builder.get_updates_connection_pool_size(50000)
    builder.pool_timeout(100)
    builder.get_updates_pool_timeout(100)
    bot = builder.bot
    builder.post_init(komutisimleristart)
    application = builder.build()
    upjob = application.job_queue
    """ Repeating Jobs """
    upjob.run_daily(gunluk, days=tuple(range(7)), time=datetime.datetime.strptime("21:55:00", '%H:%M:%S').time(), name="resetleme")
    #upjob.run_repeating(jobyedekleme, interval=300, first=10, name="yedekleme")
    upjob.run_repeating(siraclean, interval=3600, first=10, name="yedekleme")
    """ Misc """
    application.add_handler(MessageHandler(filters.Chat(-1001584743136), comment))
    application.add_handler(MessageHandler(filters.Chat(eklenti), eklentiiletisim))
    application.add_handler(MessageHandler(filters.Chat(-1001572618573), posterkomut2)) 
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, WebAppDataHandler))
    #application.add_handler(MessageHandler(filters.PHOTO & filters.UpdateType.EDITED_CHANNEL_POST | filters.VIDEO & filters.UpdateType.EDITED_CHANNEL_POST | filters.ANIMATION & filters.UpdateType.EDITED_CHANNEL_POST, poster_edit))
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
        MessageHandler(filters.UpdateType.MESSAGE & ~filters.COMMAND & filters.ChatType.PRIVATE, menu), 
        CommandHandler('start', start, filters.ChatType.PRIVATE),
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
            KANALMENU: [MessageHandler(~filters.COMMAND & filters.UpdateType.MESSAGE, kanalmenu), 
            CallbackQueryHandler(panelcall, pattern="^(panelzaman|pau-bul|pak-bul)$")],
            APIMENU: [MessageHandler(~filters.COMMAND & filters.UpdateType.MESSAGE, apimenu),  
            CallbackQueryHandler(altcall, pattern="^asite(.*)"),
            CallbackQueryHandler(panelcall, pattern="^(panelzaman|pau-bul|pak-bul)$")],
            POSTMENU: [MessageHandler(~filters.COMMAND & filters.UpdateType.MESSAGE, postmenu),
            CallbackQueryHandler(sabloncall, pattern="^(sablon)$"),
            CallbackQueryHandler(panelcall, pattern="^(panelzaman|pau-bul|pak-bul)$"),
            CallbackQueryHandler(ozelkaynakcall, pattern="^okayt(.*)"),
            CallbackQueryHandler(ozellogcall, pattern="^logokay(.*)"), 
            CallbackQueryHandler(postzamancall, pattern="^(pzayarla)$"),
            CallbackQueryHandler(callback_query, pattern="^pzamanla(.*)")], 
            EKSTRAMENU: [MessageHandler(~filters.COMMAND & filters.UpdateType.MESSAGE, ekstramenu),
            CallbackQueryHandler(begenicall, pattern="^(begeniolustur)$"),
            CallbackQueryHandler(panelcall, pattern="^(panelzaman|pau-bul|pak-bul)$"),
            CallbackQueryHandler(tekrarlisaatayarlacall, pattern="^ts-(.*)")],
            TSPOST: [MessageHandler(~filters.COMMAND, tekrarlipostayarla), CallbackQueryHandler(tsmodcall, pattern="^(tsmod-rastgele|tsmod-sirali)$")],
            PANELZAMAN: [MessageHandler(~filters.COMMAND & filters.TEXT, zaman)],
            PANELBUL: [MessageHandler(~filters.COMMAND & filters.FORWARDED | filters.TEXT & ~filters.COMMAND, panelbul)],
            TSBASLIK: [MessageHandler(~filters.COMMAND & filters.TEXT, tekrarlipostbaslikayarla)],
            BEGENI: [MessageHandler(~filters.COMMAND & filters.TEXT, begenidegistir)],
            APIDEGISTIR: [MessageHandler(~filters.COMMAND & filters.UpdateType.MESSAGE, apikayit)],
            KANALKAYDET: [MessageHandler(~filters.COMMAND & filters.UpdateType.MESSAGE, kanalkayit)],
            SABLONA: [MessageHandler(~filters.COMMAND & filters.UpdateType.MESSAGE, sabloniki)],
            PATPOST: [MessageHandler(~filters.COMMAND & filters.UpdateType.MESSAGE, pat)],
            PATZAMAN: [MessageHandler(~filters.COMMAND & filters.UpdateType.MESSAGE, patzamansaat)],
            ALTAPI: [MessageHandler(~filters.COMMAND & filters.UpdateType.MESSAGE, altakayit)],
            OZELBOTLOG: [MessageHandler(~filters.COMMAND & filters.UpdateType.MESSAGE, ozellog)],
            OZELKAYNAK: [MessageHandler(~filters.COMMAND & filters.UpdateType.MESSAGE, ozelk)],
            POSTZAMAN: [MessageHandler(~filters.COMMAND & filters.UpdateType.MESSAGE, postzaman)]
            },
        fallbacks=[MessageHandler(filters.Regex('^(↩️ Ana Menü)$') & filters.UpdateType.MESSAGE, cancel), CommandHandler('start', start, filters=~filters.UpdateType.EDITED_MESSAGE)],
        per_message=False,
        name="anaconv",
        per_chat=True
        )
    application.add_handler(conv_handler)
    """ Müşteri Komutları """
    application.add_handler(CommandHandler('panel', kaynakpanel))
    #application.add_handler(CommandHandler('kaynak', kaynakkontrol))
    application.add_handler(CommandHandler('start', start, filters.UpdateType.MESSAGE & filters.ChatType.PRIVATE))
    application.add_handler(MessageHandler(filters.Regex("^/onayla(.*)") & filters.UpdateType.CHANNEL_POST, post))
    application.add_handler(MessageHandler(filters.Regex("^(/sil)$") & filters.UpdateType.CHANNEL_POST, KanalSilKomutu))
    application.add_handler(CommandHandler('onayla', ona, filters.UpdateType.MESSAGE))
    application.add_handler(CommandHandler('sil', durdur, filters.UpdateType.MESSAGE & filters.ChatType.PRIVATE))
    """ Kaynak Komutları """
    application.add_handler(MessageHandler(filters.Regex("^/postsil(.*)") & filters.UpdateType.CHANNEL_POST, kpostsil))
    application.add_handler(CommandHandler('iptal', IptalPoster))
    application.add_handler(CommandHandler('zaman', zaman, filters.UpdateType.MESSAGE & filters.ChatType.PRIVATE))
    """ Poster """
    application.add_handler(MessageHandler(filters.PHOTO & filters.UpdateType.CHANNEL_POST | filters.VIDEO & filters.UpdateType.CHANNEL_POST | filters.ANIMATION & filters.UpdateType.CHANNEL_POST, poster))
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
    """
    for uh in collection.find_one({"_id": 0})['jobs']:
        if uh['name'].startswith("ts"):
            if uh['msgdict'].get("tetik", None) == None:
                continue
            firtime = datetime.datetime.strptime(uh['msgdict']["tetik"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.timezone('Europe/Istanbul'))
            vakit = datetime.datetime.now(pytz.timezone('Europe/Istanbul'))
            firt = firtime - vakit
            upjob.run_repeating(tekrarlipostjob, first=firt.total_seconds(), interval=3600*int(uh['msgdict']['tsaat']), name=uh['name'], data=uh['msgdict'])
            ytjcount += 1
            continue
        yjcount += 1
        uhzamani = datetime.datetime.strptime(uh['when'], '%y-%m-%d %H:%M:%S')
        upjob.run_once(zamanjob, name=str(uh['name']), data=uh['msgdict'], when=uhzamani)
    logger.warning(str(yjcount)+" Adet Tekil, "+str(ytjcount)+" Adet Tekrarlı Job Yüklendi!")
    """
    


    #upjob.run_once(jobyedekleme, when=1, name="yedekleme")

logger.info("Bot Çalışıyor...")
main()

bot = application.bot
application.run_polling(write_timeout=90, connect_timeout=90, pool_timeout=90)
bildir("Bot kapandı!")
