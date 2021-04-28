import requests
from requests import get
from os import environ
import asyncio
from time import sleep
from pymongo import MongoClient
import telebot

botapi = environ['BOT_TOKEN'] 
mongo = environ['MONGO']

cluster = MongoClient(mongo)
db = cluster["OtoPost"]
collection = db["Kanallar"]
bot = telebot.TeleBot(botapi,parse_mode='MarkDown')
print("Başlıyor")

class usre:
    def __init__(self):
        self.api = None
        self.kanal = None
    
@bot.message_handler(commands=['start'])
def start(message):
    chat = message.chat.id
    mention = "@"+message.from_user.username if message.from_user.username else message.from_user.first_name
    bot.send_message(chat, """
*✨ Merhaba* {}!

❔*Ne İşe Yarıyor?*
_Bu bot_ [Link Mahzeni'nde](https://t.me/joinchat/UYu8q0gBTUdUudDL) _paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınıza iletir._

❔*Nasıl Kullanılır?*
_1. Adım: Botu kanlınıza yönetici olarak ekleyin.
2. Adım: /kaydet komutunu kullanarak bilgilerinizi kaydedin.
3. Adım: Kanalınzda /onayla yazın.
4. Adım: Keyfini çıkarın._

*❤️ Geliştirici & Sahip : @Pharex
👨🏻‍🔧 Fix & Eklentiler : @bberc*

_👉 Kaynak kanalını değiştirmek için /kaynak yazabilirsiniz._
_👉 Post şablonunu değiştirmek için /sablon _
`👉🏻Botu durdurmak için` /sil `yazabilirsiniz`
""".format(mention), disable_web_page_preview=True)

@bot.message_handler(commands=['sil'])
def durdur(message):
    chat = message.chat.id
    user = message.from_user.id
    print(chat)
    try:
        collection.delete_one({"_id": user})
    except:
        bot.reply_to(message, "*Henüz bir kanal kaydetmemişsiniz.*")
    else:
        bot.reply_to(message, "*Kanalınız Silindi!*")

@bot.channel_post_handler(commands=['onayla'])
def post(message):
    chat = message.chat.id
    mid = message.id
    mids = mid+1
    print(chat)
    bot.reply_to(message, "Tamamdır!")
    sleep(1)
    bot.delete_message(chat, mid)
    bot.delete_message(chat, mids)

@bot.message_handler(commands=['kaydet'])
def kayit(message):
    chat = message.chat.id
    msg = bot.send_message(chat, "📝 _Lütfen_ [burdan](https://tr.link/member/tools/quick) _aldığınız API adresinizi gönderin_")
    bot.register_next_step_handler(msg, apikayit)

def apikayit(message):
    token = message.text
    mid = message.id
    mids = mid+1
    chat = message.chat.id
    bot.send_message(chat, "`👁️ API adresiniz kontrol ediliyor...`", parse_mode='MarkDown')
    s = requests.Session()
    link = s.get("https://ay.live/api")
    cookies = dict(link.cookies)
    ket = s.get(f"https://tr.link/api/?api={token}&url=yourdestinationlink.com&format=text&alias=&ct=1", cookies=cookies).text
    print(ket)
    if ket == None:
        msg = bot.edit_message_text("*✖️ Geçersiz Bir API adresi girdiniz!* _Lütfen [bu adresten](https://tr.link/member/tools/api) yeniden alın._", chat, mids)
        bot.register_next_step_handler(msg, apikayit)
        return
    usre.api = token
    msg = bot.edit_message_text("*🟢 API kaydedildi!* \n\n_Kanalınızdan herhangi bir gönderi iletin._", chat, mids)
    bot.register_next_step_handler(msg, kanalkayit)

def kanalkayit(message):
    chat = message.chat.id
    user = message.from_user.id
    
    if not message.forward_from_chat:
        msg = bot.send_message(chat, "↪️ Bunun ne olduğu hakkında bir fikrim yok! Lütfen kanaldan herhangi bir gönderi iletin.")
        bot.register_next_step_handler(msg, kanalkayit)
        return
    kanal = message.forward_from_chat.id
    usre.kanal = str(kanal)
    key = {"_id": user, "token": usre.api, "kanal": usre.kanal, "sablon": "1", "kaynak": "1"}
    bnb = collection.find_one({"_id": user})
    if bnb == None:
        collection.insert_one(key)
    else:
        collection.update_one({"_id": user}, {"$set":{"token": usre.api, "kanal": usre.kanal}})
    
    bot.reply_to(message,"*✅ Bilgileriniz Kaydedildi.*")

@bot.message_handler(commands=['sablon'])
def sablonn(message):
    chat = message.chat.id
    msg = bot.send_message(chat, "*Şablon No:1\n----------------*\n🔥{aciklama}\n\n🔱 TIKLA 👉 {link}\n\n📛 SESİ AÇ 'a tıklamayı unutma\n----------------\n\n*Şablon No:2*\n----------------\n{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06\n----------------\n\nÜstteki şablonlardan kullanmak isterseniz, istediğiniz şablonun numarasını gönderin.\n\n_Eğer kendi şablonunuzu oluşturmak isterseniz üstteki şablonlardaki gibi_ *{aciklama}* ve *{link}* _kelimelerinin bulunduğundan emin olun yoksa şablon çalışmaz_")
    bot.register_next_step_handler(msg, sabloniki)

def sabloniki(message):
    mesaj = message.text
    chat = message.chat.id
    user = message.from_user.id
    bnb = collection.find_one({"_id": user})
    if bnb == None:
        bot.send_message(chat, "Lütfen şablon kaydetmeden önce /kaydet yazarak bilgilerinizi girin!")
    else:
        collection.update_one({"_id": user}, {"$set":{"sablon": mesaj}})
        bot.send_message(chat, "Şablon kaydedildi!")

@bot.message_handler(commands=['kaynak'])
def kaynakk(message):
    chat = message.chat.id
    user = message.from_user.id
    msg = bot.send_message(chat, """*Kullanmak istediğiniz kaynak kanalınının numarasını gönderin:*
    
    *Kaynak No:1*
    [Link Mahzeni](https://t.me/joinchat/UYu8q0gBTUdUudDL)
    
    *Kaynk No:2*
    [Bedava Link](https://t.me/joinchat/MhxcfKLh3aQ4OWU0)
    
    
    """, disable_web_page_preview=True)
    bot.register_next_step_handler(msg, kaynake)

def kaynake(message):
    ktext = message.text
    chat = message.chat.id
    user = message.from_user.id
    if not ktext.isdigit():
        msg = bot.send_message(chat, "Lütfen istediğiniz kaynağın numarasını gönderin.")
        bot.register_next_step_handler(msg, kaynake)
        return
    bnb = collection.find_one({"_id": user})
    if bnb == None:
        bot.send_message(chat, "Lütfen kaynak seçmeden önce /kaydet ile bilgilerinizi kaydedin.")
    else:
        collection.update_one({"_id": user}, {"$set":{"kaynak": ktext}})
        bot.send_message(chat, "Kaynak Kaydedildi!")

@bot.channel_post_handler(content_types=['photo'])
def poster(message):
    count = 0
    chat = message.chat.id
    if chat == -1001368112299 or chat == -1001352123979:
        print(f"başlıyor ")
        mesaj = message.caption
        """  Link tespit  """
        sol = mesaj.find("http")
        sag = mesaj.find("\n", sol)
        mesajb = mesaj[sol:sag].strip()
        """  Açıklama tespit  """
        ason = mesaj.find("\n")
        aciklama = mesaj[:ason]
        """  Cookies  """
        s = requests.Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        binb = collection.find({})
        print(binb)
        """ Dosya tespit """
        medya = message.photo[0].file_id
        for hesap in binb:
            kaynak = hesap['kaynak']
            token = hesap['token']
            kanal = hesap['kanal']
            sablon = hesap['sablon']
            if kaynak == "1":
                json = s.get(f"https://ay.live/api/?api={token}&url={mesajb}&alias=&ct=1", cookies=cookies).json()
                link = json['shortenedUrl']
                print(f"{kanal} + {link} + {token}")
                try:
                    if sablon == "1":
                        sablon = f"🔥{aciklama}\n\n🔱 TIKLA 👉 {link}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                    elif sablon == "2" or sablon == "3":
                        sablon = f"{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                    else:
                        soll = sablon.split("{link}")
                        sal = soll[0].split("{aciklama}")
                        
                        sablon = f"{sal[0]}{aciklama}{sal[1]}{link}{soll[1]}"
                    
                    sleep(1)
                    bot.send_photo(kanal, medya, caption=sablon)
                except Exception as e:
                    print(e)
                    print(f"Hatalı kanal: {kanal}")
                print("Başarılı!")
            else:
                pass
            bot.send_message(-1001352123979, "{} Kanalda Post Paylaşıldı.".format(count))
    if chat == -1001122395785:
        print(f"başlıyor ")
        mesaj = message.caption
        """ Link tespit """
        sol = mesaj.find("http")
        sag = mesaj.find("\n", sol)
        mesajb = mesaj[sol:sag].strip()
        """ Açıklama tespit """
        ason = mesaj.find("\n")
        aciklama = mesaj[:ason]
        """    Cookies    """
        s = requests.Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        binb = collection.find({})
        print(binb)
        """ Dosya tespit """
        medya = message.photo[0].file_id
        for hesap in binb:
            kaynak = hesap['kaynak']
            sablon = hesap['sablon']
            sablon = str(sablon)
            token = hesap['token']
            kanal = hesap['kanal']
            print(kaynak)
            if kaynak == "2":
                json = s.get(f"https://ay.live/api/?api={token}&url={mesajb}&alias=&ct=1", cookies=cookies).json()
                link = json['shortenedUrl']
                print(f"{kanal} + {link} + {token}")
                try:
                    if sablon == "1":
                        sablon = f"🔥{aciklama}\n\n🔱 TIKLA 👉 {link}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                    elif sablon == "2" or sablon == "3":
                        sablon = f"{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                    else:
                        soll = sablon.split("{link}")
                        sal = soll[0].split("{aciklama}")
                    
                        sablon = f"{sal[0]}{aciklama}{sal[1]}{link}{soll[1]}"
                    sleep(1)
                    bot.send_photo(kanal, medya, caption=sablon)
                    count =+ 1
                except Exception as e:
                    print(f"Hatalı Kanal: {kanal}")
                    count =- 1
                print("Başarılı!")
        bot.send_message(-1001352123979, "{} Kanalda Post Paylaşıldı.".format(count))

@bot.channel_post_handler(content_types=['video'])
def poster(message):
    count = 0
    chat = message.chat.id
    if chat == -1001368112299 or chat == -1001352123979:
        print(f"başlıyor ")
        mesaj = message.caption
        """ Link tespit """
        sol = mesaj.find("http")
        sag = mesaj.find("\n", sol)
        mesajb = mesaj[sol:sag].strip()
        """ Açıklama tespit """
        ason = mesaj.find("\n")
        aciklama = mesaj[:ason]
        """    Cookies    """
        s = requests.Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        binb = collection.find({})
        print(binb)
        """ Dosya tespit """
        medya = message.video.file_id
        for hesap in binb:
            kaynak = hesap['kaynak']
            sablon = hesap['sablon']
            sablon = str(sablon)
            token = hesap['token']
            kanal = hesap['kanal']
            if kaynak == "1":
                json = s.get(f"https://ay.live/api/?api={token}&url={mesajb}&alias=&ct=1", cookies=cookies).json()
                link = json['shortenedUrl']
                print(f"{kanal} + {link} + {token}")
                try:
                    if sablon == "1":
                        sablon = f"🔥{aciklama}\n\n🔱 TIKLA 👉 {link}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                    elif sablon == "2" or sablon == "3":
                        sablon = f"{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                    else:
                        soll = sablon.split("{link}")
                        sal = soll[0].split("{aciklama}")
                    
                        sablon = f"{sal[0]}{aciklama}{sal[1]}{link}{soll[1]}"
                    sleep(1)
                    bot.send_video(kanal, medya, caption=sablon)
                    count =+ 1
                except Exception as e:
                    print(f"Hatalı Kanal: {kanal}")
                    count =- 1
                print("Başarılı!")
            else:
                pass
        bot.send_message(-1001352123979, "{} Kanalda Post Paylaşıldı.".format(count))
    elif chat == -1001122395785 or chat == -1001190898326:
        print(f"başlıyor ")
        mesaj = message.caption
        """ Link tespit """
        sol = mesaj.find("http")
        sag = mesaj.find("\n", sol)
        mesajb = mesaj[sol:sag].strip()
        """ Açıklama tespit """
        ason = mesaj.find("\n")
        aciklama = mesaj[:ason]
        """    Cookies    """
        s = requests.Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        binb = collection.find({})
        print(binb)
        """ Dosya tespit """
        medya = message.video.file_id
        for hesap in binb:
            kaynak = hesap['kaynak']
            sablon = hesap['sablon']
            sablon = str(sablon)
            token = hesap['token']
            kanal = hesap['kanal']
            print(kaynak)
            if kaynak == "2":
                json = s.get(f"https://ay.live/api/?api={token}&url={mesajb}&alias=&ct=1", cookies=cookies).json()
                link = json['shortenedUrl']
                print(f"{kanal} + {link} + {token}")
                try:
                    if sablon == "1":
                        sablon = f"🔥{aciklama}\n\n🔱 TIKLA 👉 {link}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                    elif sablon == "2" or sablon == "3":
                        sablon = f"{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                    else:
                        soll = sablon.split("{link}")
                        sal = soll[0].split("{aciklama}")
                    
                        sablon = f"{sal[0]}{aciklama}{sal[1]}{link}{soll[1]}"
                    sleep(1)
                    bot.send_video(kanal, medya, caption=sablon)
                    count =+ 1
                except Exception as e:
                    print(f"Hatalı Kanal: {kanal}")
                    count =- 1
                print("Başarılı!")
        bot.send_message(-1001352123979, "{} Kanalda Post Paylaşıldı.".format(count))


bot.enable_save_next_step_handlers(delay=4)

bot.load_next_step_handlers()

bot.polling()
