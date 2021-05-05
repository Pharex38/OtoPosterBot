import requests
from requests import get
from os import environ
import asyncio
from time import sleep
from pymongo import MongoClient
import telebot
from telebot import types

botapi = environ['BOT_TOKEN'] 
mongo = environ['MONGO']

cluster = MongoClient(mongo)
db = cluster["OtoPost"]
collection = db["Kanallar"]
bot = telebot.TeleBot(botapi,parse_mode='html')
print("Başlıyor")

karaliste = collection.find_one({"_id": 0})
kara = karaliste['kara']

sahip = 1302980840
markup = types.ForceReply(selective=False)

dugme = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)
butonbir = types.KeyboardButton('📝 Kaydet')
butoniki = types.KeyboardButton('🔧 Kaynak')
butonuc = types.KeyboardButton('📏 Şablon')
butondort = types.KeyboardButton('▶️ SFS Modu')
dugme.add(butonbir, butoniki, butonuc, butondort)

markupp = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)
buton1 = types.KeyboardButton('🔶 Yeni Kanal Ekle')
buton2 = types.KeyboardButton('❌ İptal')
buton3 = types.KeyboardButton('🗑️ Kanal Sil')
buton4 = types.KeyboardButton('♻️ API değiştir')
buton5 = types.KeyboardButton('🔗 Site değiştir')
markupp.add(buton1, buton2, buton3, buton4, buton5)

imark = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)
batinbir = types.KeyboardButton('❌ İptal')
imark.add(batinbir)

class usre:
    def __init__(self):
        self.api = None
        self.kanal = None

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user.id
    chat = message.chat.id
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    kat = collection.find_one({"_id": user})
    dagme = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)
    dagme.add(butonbir)
    mention = "@"+message.from_user.username if message.from_user.username else message.from_user.first_name
    if kat == None:
        bot.send_message(chat, """
✨ <b>Merhaba {}!</b>

❔<b>Ne İşe Yarıyor? </b>
<i>Bu bot sizin seçtiğiniz kaynak kanalında paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınıza iletir.</i>

❔<b>Nasıl Kullanılır?</b>
<i>1. Adım: Botu kanlınıza yönetici olarak ekleyin.
2. Adım: Kaydet butonunu kullanarak bilgilerinizi kaydedin.
3. Adım: <b>KANALINIZDA</b> /onayla yazın.
4. Adım: Keyfini çıkarın.</i>

<b>❤️ Geliştirici & Sahip : @Pharex
👨🏻‍🔧 Fix & Eklentiler : @bberc</b>
""".format(mention), disable_web_page_preview=True, reply_markup=dagme)
    else:
        bot.send_message(chat, """
✨ <b>Merhaba {}!</b>

❔<b>Ne İşe Yarıyor? </b>
<i>Bu bot</i><a href="https://t.me/joinchat/UYu8q0gBTUdUudDL">Link Mahzeni</a><i>'nde paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınıza iletir.</i>

❔<b>Nasıl Kullanılır?</b>
<i>1. Adım: Botu kanlınıza yönetici olarak ekleyin.
2. Adım: Kaydet butonunu kullanarak bilgilerinizi kaydedin.
3. Adım: <b>KANALINIZDA</b> /onayla yazın.
4. Adım: Keyfini çıkarın.</i>

<b>❤️ Geliştirici & Sahip : @Pharex
👨🏻‍🔧 Fix & Eklentiler : @bberc</b>
""".format(mention), disable_web_page_preview=True, reply_markup=dugme)

@bot.message_handler(commands=['sil'])
def durdur(message):
    chat = message.chat.id
    user = message.from_user.id
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    print(chat)
    try:
        collection.delete_one({"_id": user})
    except:
        bot.reply_to(message, "<b>Henüz bir kanal kaydetmemişsiniz.</b>")
    else:
        bot.reply_to(message, "<b>Kanalınız Silindi!</b>")

@bot.channel_post_handler(commands=['onayla'])
def post(message):
    chat = message.chat.id
    mid = message.id
    mids = mid+1
    print(chat)
    bot.reply_to(message, "Tamamdır!")
    sleep(1)
    try:
        bot.delete_message(chat, mid)
        bot.delete_message(chat, mids)
    except:
        pass

@bot.message_handler(content_types=['text'])
def menu(message):
    chat = message.chat.id
    user = message.from_user.id
    mesaj = message.text
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    if mesaj == "🔧 Kaynak":
        msg = bot.send_message(chat, """<b>Kullanmak istediğiniz kaynak kanalınının numarasını gönderin:
    
    Kaynak No:1</b>
    <a href="https://t.me/joinchat/UYu8q0gBTUdUudDL">Link Mahzeni</a>
    
    <b>Kaynak No:2</b>
    <a href="https://t.me/joinchat/MhxcfKLh3aQ4OWU0">Bedava Link</a>
    
    <b>Kaynak No:3</b>
    <a href="https://t.me/joinchat/VNbV7mqzwbA47wtT">Link Evi</a>

<b>❗Hepsinden atsın fütursuzca kanalımı sikmek istiyorum diyorsan 0 yaz</b>
    
    
    """, disable_web_page_preview=True, reply_markup=imark)
        bot.register_next_step_handler(msg, kaynake)
        return
    if mesaj == "📏 Şablon":
        bot.send_message(chat, """<b>Şablon No:1</b>
    ----------------
🔥{aciklama}

🔱 TIKLA 👉 {link}

📛 SESİ AÇ 'a tıklamayı unutma
----------------

<b>Şablon No:2</b>
----------------
{aciklama} 

𝙇𝙄𝙉𝙆🔗 {link}

🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.

📌 Link Nasıl Açılır Bilmiyorsanız

👉 @linkgec06
----------------

Üstteki şablonlardan kullanmak isterseniz, istediğiniz şablonun numarasını gönderin.""", reply_markup=markup)
        msg = bot.send_message(chat, "<i>Eğer kendi şablonunuzu oluşturmak isterseniz üstteki şablonlardaki gibi</i> <b>{aciklama}</b> ve <b>{link}</b> <i>kelimelerinin bulunduğundan emin olun yoksa şablon çalışmaz</i>", reply_markup=imark)
        bot.register_next_step_handler(msg, sabloniki)
        return
    if mesaj == "📝 Kaydet":
        kayitli = 0
        chat = message.chat.id
        bina = collection.find_one({"_id": chat})
        try:
            for chan in bina['kanal']:
                try:
                    kbilgi = bot.get_chat(chan)
                except Exception as e:
                    print(e)
                    collection.update_one({"_id": chat}, {"$pull": {"kanal": chan}})
                    print("Kanal silindi")
                else:    
                    bot.send_message(chat, """Kayit No: {}\n\nKanalınız: <a href="{}">{}</a>""".format(kayitli+1, kbilgi.invite_link, kbilgi.title))
                kayitli = kayitli + 1
        except Exception as e:
            print(e)
            pass
        try:
            tokenn = bina['token']
        except:
            msg = bot.send_message(chat, """📝 <i>Lütfen</i> <a href="https://tr.link/member/tools/quick">burdan</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=markup)
            bot.register_next_step_handler(msg, apikayit)
            return
        else:
            site = bina['site']
            if site == "1":
                site = "TRLink"
            if site == "2":
                site = "PND.TL"
            if site == "3":
                site = "Exe.io"
            if site == "4":
                site = "Ouo.io"
            if site == "5":
                site = "Pubiza"
            msg = bot.send_message(chat, "♦️Kayıtlı API: {}\nSite: {}\nToplam: {}".format(tokenn, site, kayitli), reply_markup=markupp)
            bot.register_next_step_handler(msg, kayitapi)
            return
    if mesaj == "▶️ SFS Modu":
        mod = collection.find_one({"_id": user})
        if mod['kaynak'] == "9":
            try:
                collection.update_one({"_id": user}, {"$set": {"kaynak": mod['eski']}})
            except:
                pass
            bot.send_message(chat, "SFS modu durduruldu", reply_markup=dugme)
            return
        else:
            collection.update_one({"_id": user}, {"$set": {"eski": mod['kaynak']}})
            collection.update_one({"_id": user}, {"$set": {"kaynak": "9"}})
            bot.send_message(chat, "Kanallarınız SFS moduna alındı. Siz modu kapatana kadar yeni post atılmayacak.", reply_markup=dugme)
            return
    if mesaj == "Post Oluştur":
        if not user == sahip:
            bot.send_message(chat, "Bu komut şuanda bakımda")
            return
        msg = bot.send_message(chat, "Post at")
        bot.register_next_step_handler(msg, pat)
        return
    bot.send_message(chat, "<i>Lütfen alttaki butonları kullan</i>", reply_markup=dugme)
    
def kaynake(message):
    ktext = message.text
    chat = message.chat.id
    user = message.from_user.id
    if message.text == None:
        msg = bot.send_message(chat, "Lütfen istediğiniz kaynağın numarasını gönderin.")
        bot.register_next_step_handler(msg, kaynake)
        return
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    if not ktext.isdigit():
        msg = bot.send_message(chat, "Lütfen istediğiniz kaynağın numarasını gönderin.")
        bot.register_next_step_handler(msg, kaynake)
        return
    bnb = collection.find_one({"_id": user})
    if bnb == None:
        bot.send_message(chat, "Lütfen kaynak seçmeden önce Kaydet butonu ile bilgilerinizi kaydedin.", reply_markup=dugme)
    else:
        collection.update_one({"_id": user}, {"$set":{"kaynak": ktext}})
        bot.send_message(chat, "Kaynak Kaydedildi!", reply_markup=dugme)

def sabloniki(message):
    mesaj = message.text
    chat = message.chat.id
    user = message.from_user.id
    if message.text == None:
        if mesaj.find("{link}") == -1 or mesaj.find("{aciklama}") == -1:
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}" ve "{aciklama}" bulunduğudan emin olun.</i> """)
            bot.register_next_step_handler(msg, sabloniki)
            return
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    if not mesaj.isdigit():
        if mesaj.find("{link}") == -1 or mesaj.find("{aciklama}") == -1:
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}" ve "{aciklama}" bulunduğudan emin olun.</i> """)
            bot.register_next_step_handler(msg, sabloniki)
            return
    bnb = collection.find_one({"_id": user})
    if bnb == None:
        bot.send_message(chat, "Lütfen şablon kaydetmeden önce Kaydet butonu ile bilgilerinizi girin!", reply_markup=dugme)
    else:
        collection.update_one({"_id": user}, {"$set":{"sablon": mesaj}})
        bot.send_message(chat, "Şablon kaydedildi!", reply_markup=dugme)

def kayitapi(message):
    chat = message.chat.id
    mesaj = message.text
    if mesaj == "🗑️ Kanal Sil":
        msg = bot.send_message(chat, "Silmek istediğiniz kanalın kayıt numarasını girin.", reply_markup=imark)
        bot.register_next_step_handler(msg, ksil)
        return
    if mesaj == "♻️ API değiştir":
        msg = bot.send_message(chat, "Yeni API adresinizi girin.", reply_markup=imark)
        bot.register_next_step_handler(msg, apikayit)
        return
    if mesaj == "❌ İptal":
        msg = bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    if mesaj == "🔗 Site değiştir":
        msg = bot.send_message(chat, "<i>Kullanmak istediğiniz sitenin numarasını girin:\n\n<b>    No:1</b>\n    TRLink (Varsayılan)\n\n<b>    No:2</b>\n    PND.TL\n\n<b>    No:3</b>\n    Exe.io\n\n<b>    No:4</b>\n    Ouo.io\n\n<b>    No:5</b>\n    Pubiza</i>\n \nㅤ\nㅤ", reply_markup=imark)
        bot.register_next_step_handler(msg, sitekayit)
        return
    if mesaj == "🔶 Yeni Kanal Ekle":
        bol = collection.find_one({"_id": chat})
        if len(bol['kanal']) > 2:
            bot.send_message(chat, "<i>Üzgünüm en fazla 3 kanal kaydedebilirsiniz.</i>", reply_markup=imark)
            return
        msg = bot.send_message(chat, """📝 <i>Lütfen kanalınızdan bir gönderi iletin.</i>""", reply_markup=imark)
        bot.register_next_step_handler(msg, kanalkayit)
        return
    msg = bot.send_message(chat, "Lütfen alttaki butonları kullanın.", reply_markup=markupp)
    bot.register_next_step_handler(msg, kayitapi)

def ksil(message):
    user = message.from_user.id
    chat = message.chat.id
    if message.text == None:
        msg = bot.send_message(chat, "Lütfen geçerli bir numara verin")
        bot.register_next_step_handler(msg, ksil)
        return
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    mesaj = int(message.text) - 1
    if not message.text.isdigit():
        bot.send_message(chat, "Lütfen geçerli bir numara verin")
        return
    bul = collection.find_one({"_id": user})
    x = bul['kanal']
    try:
        collection.update_one({"_id": user}, {"$pull": {"kanal": x[mesaj]}})
    except:
        bot.send_message(chat, "Yanlış bir numara girdiniz.", reply_markup=dugme)
    else:
        bot.send_message(chat, "Kanalınız silindi.", reply_markup=dugme)

def apikayit(message):
    token = message.text
    mid = message.id
    user = message.from_user.id
    mids = mid+1
    chat = message.chat.id
    if message.text == None:
        msg = bot.send_message(chat, "Lütfen geçerli bir API verin.")
        bot.register_next_step_handler(msg, apikayit)
        return
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    bnb = collection.find_one({"_id": user})
    key = {"_id": user, "token": token, "kanal": [], "sablon": "1", "kaynak": "1", "site": "1"}
    if bnb == None:
        collection.insert_one(key)
    else:
        collection.update_one({"_id": user}, {"$set": {"token": token}})
    bot.send_message(chat, "<b>🟢 API kaydedildi!</b>", reply_markup=dugme)

def kanalkayit(message):
    chat = message.chat.id
    user = message.from_user.id
    kanals = []
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    if not message.forward_from_chat:
        msg = bot.send_message(chat, "↪️ Bunun ne olduğu hakkında bir fikrim yok! Lütfen kanaldan herhangi bir gönderi iletin.")
        bot.register_next_step_handler(msg, kanalkayit)
        return
    kanal = message.forward_from_chat.id
    kanals.append(str(kanal))
    y = collection.find_one({"_id": user})
    collection.update_one({"_id": user}, {"$push":{"kanal": str(kanal)}})
    bot.reply_to(message,"<b>🟢Kanalınız Kaydedildi.</b>", reply_markup=dugme)

def pat(message):
    chat = message.chat.id
    user = message.from_user.id
    if message.content_type == "text":
        msg = bot.send_message(chat, "Lütfen paylaşmamı istediğin postu at")
        bot.register_next_step_handler(msg, pat)
        return
    mesaj = message.caption
    if message.content_type == "video":
        fid = message.video.file_id
    if message.content_type == "photo":
        fid = message.photo[0].file_id
    """Açıklama Tespit"""
    pson = mesaj.find("\n")
    paciklama = mesaj[:pson]
    """Link Tespit"""
    psol = mesaj.find("http")
    psag = mesaj.find("\n")
    plink = mesaj[psol:psag].strip()
    pathesap = collection.find_one({"_id": user})
    s = requests.Session()
    link = s.get("https://ay.live/api")
    cookies = dict(link.cookies)
    ptoken = pathesap['token']
    psablon = pathesap['sablon']
    psite = pathesap['site']
    if psite == "1":
        pjson = s.get(f"https://ay.live/api/?api={ptoken}&url={plink}&alias=&ct=1", cookies=cookies).json()
        plink = pjson['shortenedUrl']
    if psite == "2":
        pjson = s.get(f"https://www.pnd.tl/api?api={ptoken}&url={plink}&category=6").json()
        print(plink)
        print(ptoken)
        print(pjson)
        plink = pjson['shortenedUrl']
    if psite == "3":
        pjson = s.get(f"https://exe.io/api?api={ptoken}&url={plink}").json()
        plink = pjson['shortenedUrl']
    if psite == "4":
        plink = s.get(f"http://ouo.io/api/{ptoken}?s={plink}").text
    if psite == "5":
        plink = s.get(f"http://pubiza.com/api.php?token={ptoken}&url={plink}&ads_type=adult").text
    if psablon == "1":
        psablon = f"🔥{paciklama}\n\n🔱 TIKLA 👉 {plink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
    elif psablon == "2" or psablon == "3":
        psablon = f"{paciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {plink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
    else:
        psoll = psablon.split("{link}")
        psal = psoll[0].split("{aciklama}")
        psablon = f"{psal[0]}{paciklama}{psal[1]}{plink}{psoll[1]}"
    print(psablon)
    
def sitekayit(message):
    chat = message.chat.id
    user = message.from_user.id
    if message.text == None:
        msg = bot.send_message(chat, "Lütfen doğru bir numara girin")
        bot.register_next_step_handler(msg, sitekayit)
        return
    if message.text == "❌ İptal":
        bot.send_message(chat, "İptal Edildi.", reply_markup=dugme)
        return
    mesaj = str(message.text)
    if not message.text.isdigit() or len(mesaj) > 1:
        msg = bot.send_message(chat, "Lütfen doğru bir numara girin")
        bot.register_next_step_handler(msg, sitekayit)
        return
    collection.update_one({"_id": user}, {"$set": {"site": mesaj}})
    bot.send_message(chat, "Site Kaydedildi\n\nAPI adresinizi seçtiğiniz siteye göre değiştirmeyi unutmayın.", reply_markup=dugme)

@bot.channel_post_handler(content_types=['photo'])
def poster(message):
    count = 0
    bcount = 0
    ccount = 0
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
            user = hesap['_id']
            site = hesap["site"]
            if kaynak == "1" or kaynak == "0" or kaynak == "5":
                if site == "1":
                    json = s.get(f"https://ay.live/api/?api={token}&url={mesajb}&alias=&ct=1", cookies=cookies).json()
                    link = json['shortenedUrl']
                if site == "2":
                    json = s.get(f"https://www.pnd.tl/api?api={token}&url={mesajb}&category=6").json()
                    link = json['shortenedUrl']
                if site == "3":
                    json = s.get(f"https://exe.io/api?api={token}&url={mesajb}").json()
                    link = json['shortenedUrl']
                if site == "4":
                    link = s.get(f"http://ouo.io/api/{token}?s={mesajb}").text
                if site == "5":
                    link = s.get(f"http://pubiza.com/api.php?token={token}&url={mesajb}&ads_type=adult").text
                print(f"{kanal} + {link} + {token}")
                if sablon == "1":
                    sablon = f"🔥{aciklama}\n\n🔱 TIKLA 👉 {link}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif sablon == "2" or sablon == "3":
                    sablon = f"{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                else:
                    soll = sablon.split("{link}")
                    sal = soll[0].split("{aciklama}")
                        
                    sablon = f"{sal[0]}{aciklama}{sal[1]}{link}{soll[1]}"
                    
                sleep(1)
                for kan in kanal:
                    try:
                        bot.send_photo(kan, medya, caption=sablon)
                        count = count + 1
                    except Exception as e:
                        print(e)
                        print(f"Hatalı kanal: {kanal}")
                        e = str(e)
                        if e.find("bot is not a member") != -1:
                            collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                            bot.send_message(user, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            print(f"{kanal} kayıtlardan silindi.")
                print("Başarılı!")
            else:
                pass
        bot.send_message(-1001352123979, "Link Mahzeni kanalından, {} Kanalda Foto Post Paylaşıldı.".format(count))
    elif chat == -1001122395785:
        print(f"başlıyor ")
        bmesaj = message.caption
        """ Link tespit """
        bsol = bmesaj.find("http")
        bsag = bmesaj.find("\n", bsol)
        bmesajb = bmesaj[bsol:bsag].strip()
        """ Açıklama tespit """
        bason = bmesaj.find("\n")
        baciklama = mesaj[:bason]
        """    Cookies    """
        s = requests.Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        bbinb = collection.find({})
        print(bbinb)
        """ Dosya tespit """
        bmedya = message.photo[0].file_id
        for bhesap in bbinb:
            bkaynak = bhesap['kaynak']
            bsablon = bhesap['sablon']
            bsablon = str(bsablon)
            btoken = bhesap['token']
            bkanal = bhesap['kanal']
            buser = bhesap['_id']
            bsite = bhesap['site']
            print(bkaynak)
            sleep(2)
            if bkaynak == "2" or bkaynak == "0" or bkaynak == "5":
                if site == "1":
                    bjson = s.get(f"https://ay.live/api/?api={btoken}&url={bmesajb}&alias=&ct=1", cookies=cookies).json()
                    blink = bjson['shortenedUrl']
                if bsite == "2":
                    bjson = s.get(f"https://www.pnd.tl/api?api={btoken}&url={bmesajb}&category=6").json()
                    blink = bjson['shortenedUrl']
                if bsite == "3":
                    bjson = s.get(f"https://exe.io/api?api={btoken}&url={bmesajb}").json()
                    blink = bjson['shortenedUrl']
                if bsite == "4":
                    blink = s.get(f"http://ouo.io/api/{btoken}?s={bmesajb}").text
                if bsite == "5":
                    blink = s.get(f"http://pubiza.com/api.php?token={btoken}&url={bmesajb}&ads_type=adult").text
                print(f"{bkanal} + {blink} + {btoken}")
                if bsablon == "1":
                    bsablon = f"🔥{baciklama}\n\n🔱 TIKLA 👉 {blink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif bsablon == "2" or bsablon == "3":
                    bsablon = f"{baciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {blink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                else:
                    bsoll = bsablon.split("{link}")
                    bsal = bsoll[0].split("{aciklama}")
                    
                    bsablon = f"{bsal[0]}{baciklama}{bsal[1]}{blink}{bsoll[1]}"
                sleep(1)
                for bkan in bkanal:
                    try:
                        bot.send_photo(bkan, bmedya, caption=bsablon)
                        bcount = bcount + 1
                    except Exception as e:
                        print(e)
                        print(f"Hatalı kanal: {bkanal}")
                        e = str(e)
                        print(e)
                        if e.find("bot is not a member") != -1:
                            collection.update_one({"_id": buser}, {"$pull": {"kanal": bkan}})
                            bot.send_message(buser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            print(f"{bkanal} kayıtlardan silindi.")
                    
                print("Başarılı!")
        bot.send_message(-1001352123979, "Bedava Link kaynağından, {} Kanalda Foto Post Paylaşıldı.".format(bcount))
    elif chat == -1001423365614: #Link Evi
        print(f"başlıyor ")
        cmesaj = message.caption
        """ Link tespit """
        csol = cmesaj.find("http")
        csag = cmesaj.find("\n", csol)
        cmesajb = cmesaj[csol:csag].strip()
        """ Açıklama tespit """
        cason = cmesaj.find("\n")
        caciklama = cmesaj[:cason]
        """    Cookies    """
        s = requests.Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        cbinb = collection.find({})
        print(cbinb)
        """ Dosya tespit """
        cmedya = message.photo[0].file_id
        for chesap in cbinb:
            ckaynak = chesap['kaynak']
            csablon = chesap['sablon']
            csablon = str(csablon)
            ctoken = chesap['token']
            ckanal = chesap['kanal']
            cuser = chesap['_id']
            csite = chesap['site']
            print(ckaynak)
            sleep(2)
            if ckaynak == "3" or ckaynak == "0":
                if csite == "1":
                    bjson = s.get(f"https://ay.live/api/?api={ctoken}&url={cmesajb}&alias=&ct=1",
                                  cookies=cookies).json()
                    clink = bjson['shortenedUrl']
                if csite == "2":
                    bjson = s.get(f"https://www.pnd.tl/api?api={ctoken}&url={cmesajb}&category=6").json()
                    clink = bjson['shortenedUrl']
                if csite == "3":
                    bjson = s.get(f"https://exe.io/api?api={ctoken}&url={cmesajb}").json()
                    clink = bjson['shortenedUrl']
                if csite == "4":
                    clink = s.get(f"http://ouo.io/api/{ctoken}?s={cmesajb}").text
                if csite == "5":
                    clink = s.get(f"http://pubiza.com/api.php?token={ctoken}&url={cmesajb}&ads_type=adult").text
                print(f"{ckanal} + {clink} + {ctoken}")
                if csablon == "1":
                    csablon = f"🔥{caciklama}\n\n🔱 TIKLA 👉 {clink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif csablon == "2" or csablon == "3":
                    csablon = f"{caciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {clink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                else:
                    csoll = csablon.split("{link}")
                    csal = csoll[0].split("{aciklama}")

                    csablon = f"{csal[0]}{caciklama}{csal[1]}{clink}{csoll[1]}"
                sleep(1)
                for ckan in ckanal:
                    try:
                        bot.send_photo(ckan, cmedya, caption=csablon)
                        ccount = ccount + 1
                    except Exception as e:
                        print(e)
                        print(f"Hatalı kanal: {ckanal}")
                        e = str(e)
                        print(e)
                        if e.find("bot is not a member") != -1:
                            collection.update_one({"_id": cuser}, {"$pull": {"kanal": ckan}})
                            bot.send_message(cuser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            print(f"{ckanal} kayıtlardan silindi.")

                print("Başarılı!")
        bot.send_message(-1001352123979, "Link Evi kaynağından, {} Kanalda Foto Post Paylaşıldı.".format(ccount))


@bot.channel_post_handler(content_types=['video'])
def poster(message):
    count = 0
    bcount = 0
    ccount = 0
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
            user = hesap['_id']
            site = hesap['site']
            if kaynak == "1" or kaynak == "0" or kaynak == "5":
                if site == "1":
                    json = s.get(f"https://ay.live/api/?api={token}&url={mesajb}&alias=&ct=1", cookies=cookies).json()
                    link = json['shortenedUrl']
                if site == "2":
                    json = s.get(f"https://www.pnd.tl/api?api={token}&url={mesajb}&category=6").json()
                    link = json['shortenedUrl']
                if site == "3":
                    json = s.get(f"https://exe.io/api?api={token}&url={mesajb}").json()
                    link = json['shortenedUrl']
                if site == "4":
                    link = s.get(f"http://ouo.io/api/{token}?s={mesajb}").text
                if site == "5":
                    link = s.get(f"http://pubiza.com/api.php?token={token}&url={mesajb}&ads_type=adult").text
                if sablon == "1":
                    sablon = f"🔥{aciklama}\n\n🔱 TIKLA 👉 {link}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif sablon == "2" or sablon == "3":
                    sablon = f"{aciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {link}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                else:
                    soll = sablon.split("{link}")
                    sal = soll[0].split("{aciklama}")

                    sablon = f"{sal[0]}{aciklama}{sal[1]}{link}{soll[1]}"
                sleep(1)

                print(f"{kanal} + {link} + {token}")
                for kan in kanal:
                    try:
                        bot.send_video(kan, medya, caption=sablon)
                        count = count + 1
                    except Exception as e:
                        print(e)
                        print(f"Hatalı kanal: {kanal}")
                        e = str(e)
                        if e.find("bot is not a member") != -1:
                            collection.update_one({"_id": user}, {"$pull": {"kanal": kan}})
                            bot.send_message(user, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            print(f"{kanal} kayıtlardan silindi.")
            else:
                pass
        bot.send_message(-1001352123979, "Link Mahzeni kaynağından, {} Kanalda Video Post Paylaşıldı.".format(count))
    elif chat == -1001122395785 or chat == -1001190898326:
       
        print(f"başlıyor ")
        bmesaj = message.caption
        """ Link tespit """
        bsol = bmesaj.find("http")
        bsag = bmesaj.find("\n", bsol)
        bmesajb = bmesaj[bsol:bsag].strip()
        """ Açıklama tespit """
        bason = bmesaj.find("\n")
        baciklama = bmesaj[:bason]
        """    Cookies    """
        s = requests.Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        bbinb = collection.find({})
        print(bbinb)
        """ Dosya tespit """
        bmedya = message.video.file_id
        for bhesap in bbinb:
            bkaynak = bhesap['kaynak']
            bsablon = bhesap['sablon']
            bsablon = str(bsablon)
            btoken = bhesap['token']
            bkanal = bhesap['kanal']
            buser = bhesap['_id']
            bsite = bhesap['site']
            print(bkaynak)
            sleep(1)
            if bkaynak == "2" or bkaynak == "0" or bkaynak == "5":
                if bsite == "1":
                    bjson = s.get(f"https://ay.live/api/?api={btoken}&url={bmesajb}&alias=&ct=1", cookies=cookies).json()
                    blink = bjson['shortenedUrl']
                if bsite == "2":
                    bjson = s.get(f"https://www.pnd.tl/api?api={btoken}&url={bmesajb}&category=6").json()
                    blink = bjson['shortenedUrl']
                if bsite == "3":
                    bjson = s.get(f"https://exe.io/api?api={btoken}&url={bmesajb}").json()
                    blink = bjson['shortenedUrl']
                if bsite == "4":
                    blink = s.get(f"http://ouo.io/api/{btoken}?s={bmesajb}").text
                if bsite == "5":
                    blink = s.get(f"http://pubiza.com/api.php?token={btoken}&url={bmesajb}&ads_type=adult").text
                print(f"{bkanal} + {blink} + {btoken}")
                if bsablon == "1":
                        bsablon = f"🔥{baciklama}\n\n🔱 TIKLA 👉 {blink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif bsablon == "2" or bsablon == "3":
                    bsablon = f"{baciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {blink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                else:
                    bsoll = bsablon.split("{link}")
                    bsal = bsoll[0].split("{aciklama}")
                    
                    bsablon = f"{bsal[0]}{baciklama}{bsal[1]}{blink}{bsoll[1]}"
                    
                for bkan in bkanal:
                    try:
                        bot.send_video(bkan, bmedya, caption=bsablon)
                        bcount = bcount + 1
                    except Exception as e:
                        print(e)
                        print(f"Hatalı kanal: {bkanal}")
                        e = str(e)
                        if e.find("bot is not a member") != -1:
                            collection.update_one({"_id": buser}, {"$pull": {"kanal": bkan}})
                            bot.send_message(buser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            print(f"{bkanal} kayıtlardan silindi.")
                    
                print("Başarılı!")
        bot.send_message(-1001352123979, "Bedava Link kanalından, {} Kanalda Video Post Paylaşıldı.".format(bcount))
    if chat == -1001423365614: #Link Evi
        print(f"başlıyor ")
        cmesaj = message.caption
        """ Link tespit """
        csol = cmesaj.find("http")
        csag = cmesaj.find("\n", csol)
        cmesajc = cmesaj[csol:csag].strip()
        """ Açıklama tespit """
        cason = cmesaj.find("\n")
        caciklama = cmesaj[:cason]
        """    Cookies    """
        s = requests.Session()
        link = s.get("https://ay.live/api")
        cookies = dict(link.cookies)
        ccinc = collection.find({})
        print(ccinc)
        """ Dosya tespit """
        cmedya = message.video.file_id
        for chesap in ccinc:
            ckaynak = chesap['kaynak']
            csaclon = chesap['sablon']
            csaclon = str(csaclon)
            ctoken = chesap['token']
            ckanal = chesap['kanal']
            cuser = chesap['_id']
            csite = chesap['site']
            print(ckaynak)
            sleep(1)
            if ckaynak == "3" or ckaynak == "0":
                if csite == "1":
                    cjson = s.get(f"https://ay.live/api/?api={ctoken}&url={cmesajc}&alias=&ct=1", cookies=cookies).json()
                    clink = cjson['shortenedUrl']
                if csite == "2":
                    cjson = s.get(f"https://www.pnd.tl/api?api={ctoken}&url={cmesajc}&category=6").json()
                    clink = cjson['shortenedUrl']
                if csite == "3":
                    cjson = s.get(f"https://exe.io/api?api={ctoken}&url={cmesajc}").json()
                    clink = cjson['shortenedUrl']
                if csite == "4":
                    clink = s.get(f"http://ouo.io/api/{ctoken}?s={cmesajc}").text
                if csite == "5":
                    clink = s.get(f"http://puciza.com/api.php?token={ctoken}&url={cmesajc}&ads_type=adult").text
                print(f"{ckanal} + {clink} + {ctoken}")
                if csaclon == "1":
                    csaclon = f"🔥{caciklama}\n\n🔱 TIKLA 👉 {clink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                elif csaclon == "2" or csaclon == "3":
                    csaclon = f"{caciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {clink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır cilmiyorsanız\n\n👉 @linkgec06"
                else:
                    csoll = csaclon.split("{link}")
                    csal = csoll[0].split("{aciklama}")

                    csaclon = f"{csal[0]}{caciklama}{csal[1]}{clink}{csoll[1]}"

                for ckan in ckanal:
                    try:
                        bot.send_video(ckan, cmedya, caption=csaclon)
                        ccount = ccount + 1
                    except Exception as e:
                        print(e)
                        print(f"Hatalı kanal: {ckanal}")
                        e = str(e)
                        if e.find("bot is not a memcer") != -1:
                            collection.update_one({"_id": cuser}, {"$pull": {"kanal": ckan}})
                            bot.send_message(cuser, "botu kanalınızdan çıkardığınız için kanalınız silindi.")
                            print(f"{ckanal} kayıtlardan silindi.")

                print("caşarılı!")
        bot.send_message(-1001352123979, "Link Evi kanalından, {} Kanalda Video Post Paylaşıldı.".format(ccount))



bot.enable_save_next_step_handlers(delay=4)

bot.load_next_step_handlers()

bot.polling()
