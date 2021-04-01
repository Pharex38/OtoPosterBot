from requests import get

SUDOUID = 1302980840
from telegram import *

BRAIN = []
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import os
import sqlite3 as sql
from logging import basicConfig, getLogger, INFO
import pymongo
from pymongo import MongoClient

GENDER, PHOTO, LOCATION, TOKEN = range(4)

basicConfig(format="%(asctime)s - @TRLinkShortener - %(levelname)s - %(message)s",
            level=INFO)
LOGS = getLogger(__name__)

LOGS.info("Bot Çalışıyor...")

API_KEY = os.environ['BOT_TOKEN']


cluster = pymongo.MongoClient("mongodb+srv://Pharex:545456@cluster0.teii1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["txt"]
collection = db["txt"]


def yardim_komut(update, context):
    user = update.message.from_user
    update.message.reply_text(
        f"_Merhaba_ *{user.first_name}*_, Link Kısaltma botuna hoşgeldin. Bu bot ile TRLink API adresini kullanarak Link Kısaltabilirsin._ *API adresini girmek için /token yaz.\n\n🛸 Sahip : @Pharex \n❤️ Fix & Eklentiler: @bberc* \n\n ❗ _Bu bot ile kısaltılan linkler +18 kategorisinde kısaltılır farklı bir kategori de link paylaşıyorsanız CPM'iniz düşebilir._ \n\n*Çok isterseniz /bagis atabilirsiniz.*",
        parse_mode=ParseMode.MARKDOWN)


def start(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        '_Lütfen_ [burdan](https://tr.link/member/tools/quick) _aldığınız API adresinizi gönderin_',
        parse_mode=ParseMode.MARKDOWN)

    return GENDER


def bagis_komut(update, context):
    update.message.reply_text(
        f"*🥰Aylık 20₺ bağış toplayabilirsek başka sunucuya geçeceğiz. Başka sunucuya geçince sürekli API girmenize gerek kalmayacak.*\n\n🏧Papara: `1666982412`\n🏦İninal: `4003140030544`",
        parse_mode=ParseMode.MARKDOWN)


if os.path.exists("learning-data-root.check"):
    os.remove("learning-data-root.check")
else:
    LOGS.info("Braincheck dosyası yok, getiriliyor...")

URL = 'https://gitlab.com/must4f/VaveylaData/-/raw/main/learning-data-root.check'
with open('learning-data-root.check', 'wb') as load:
    load.write(get(URL).content)
DB = sql.connect("learning-data-root.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()


def gender(update: Update, _: CallbackContext) -> int:
    mesaj = update.message.text
    user = update.message.from_user
    key = {"_id": user.id, "api": f"{mesaj}"}
    collection.insert_one(key)
    update.message.reply_text(f'*API Kaydedildi. Kısaltmam için bana bir link gönder.* _Tekrar girmek istersen_ /token _yazmanız yeterli._', parse_mode=ParseMode.MARKDOWN)

    return ConversationHandler.END


for i in ALL_ROWS:
    BRAIN.append(i[0])
sql.connect("learning-data-root.check").close()
links = 0


def handle_message(update, context):
    user = update.message.from_user
    keyler = collection.find_one({"_id": user.id})
    text = update.message.text
    for key in keyler:
        token = key["api"]
        if text.startswith("https") or text.startswith("www") or text.startswith("http"):
            if text.startswith("https://mega.nz/"):
                json = get(f"https://ay.live/api/?api={token}&url={text}&alias=&format=text&ct=1").json()
                if not json["status"] == "success":
                    update.message.reply_text('`Bir hata oluştu!`', parse_mode=ParseMode.MARKDOWN)
                   return
                link = json["shortenedUrl"]
                update.message.reply_text(f'*Linkiniz:\n*'

                                      f'🔹 `{link}`', parse_mode=ParseMode.MARKDOWN)
                links += 1
                return links
            else:
                json = get(f"https://ay.live/api/?api={token}&url={text}&alias=&ct=1").json()
                link = json["shortenedUrl"]
                if not json["status"] == "success":
                    update.message.reply_text(
                    f"Link kısaltılamadı API adresiniz hatalı olabilir, lütfen /token yazarak API adresinizi yeniden girin")
                if json == None:
                    update.message.reply_text('<s>🥴 TRLink mesajıma cevap vermedi!</s>', parse_mode=ParseMode.HTML)
                    return
                update.message.reply_text(f'*Linkiniz:\n\n*'

                                          f'🔹 `{link}`', parse_mode=ParseMode.MARKDOWN)
                links += 1
                return links
        else:
            update.message.reply_text(f"_Lütfen kısaltmam için bir link gönder_", parse_mode=ParseMode.MARKDOWN)


def kontrok(update, context):
    global links
    kullanici = update.message.from_user
    uid = kullanici.id
    users = []
    for usre in os.listdir("./txtler/"):
        if not usre.endswith(".py") or usre.startswith("_"):
            continue
        users.append(f"{usre.replace('.txt', '')}")
    if uid == BRAIN or uid == SUDOUID:
        update.message.reply_text("""
🆔 *Update Sonrası Kullanıcılar:* `{users}`
🆔 *Update Sonrası Kısaltılan Link:* `{links}`""", parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("Bunları seninle paylaşamam!!")


def error(update, context):
    LOGS.info(f"\n\nGerçekleşen hata : Update {update} caused error {context.error}")


def cancel(update: Update, _: CallbackContext) -> int:
    update.message.reply_text('İptal Edildi.')

    return ConversationHandler.END


def main():
    updater = Updater(API_KEY, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('token', start)],
        states={
            GENDER: [MessageHandler(Filters.text, gender)],

        },
        fallbacks=[CommandHandler('iptal', cancel)],
    )

    dp.add_handler(CommandHandler("start", yardim_komut))
    dp.add_handler(CommandHandler("stats", kontrok))
    dp.add_handler(CommandHandler("bagis", bagis_komut))
    #    dp.add_handler(CommandHandler("token", token_command))

    dp.add_handler(conv_handler)

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


main()
