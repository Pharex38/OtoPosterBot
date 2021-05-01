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

class usre:
    def __init__(self):
        self.api = None
        self.kanal = None
    
@bot.message_handler(commands=['start'])
def start(message):
    chat = message.chat.id
    user = message.from_user.id
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    mention = "@"+message.from_user.username if message.from_user.username else message.from_user.first_name
    bot.send_message(chat, """
✨ <b>Merhaba {}!</b>

❔<b>Ne İşe Yarıyor? </b>
<i>Bu bot</i><a href="https://t.me/joinchat/UYu8q0gBTUdUudDL">Link Mahzeni</a><i>'nde paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınıza iletir.</i>

❔<b>Nasıl Kullanılır?</b>
<i>1. Adım: Botu kanlınıza yönetici olarak ekleyin.
2. Adım: /kaydet komutunu kullanarak bilgilerinizi kaydedin.
3. Adım: KANALINIZDA /onayla yazın.
4. Adım: Keyfini çıkarın.</i>

<b>❤️ Geliştirici & Sahip : @Pharex
👨🏻‍🔧 Fix & Eklentiler : @bberc</b>

<i>👉 Kaynak kanalını değiştirmek için /kaynak yazabilirsiniz.
👉 Post şablonunu değiştirmek için /sablon 
👉🏻Botu durdurmak için /sil yazabilirsiniz</i>
""".format(mention), disable_web_page_preview=True)

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
    user = message.from_user.id
    chat = message.chat.id
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    mid = message.id
    mids = mid+1
    print(chat)
    bot.reply_to(message, "Tamamdır!")
    sleep(1)
    bot.delete_message(chat, mid)
    bot.delete_message(chat, mids)

@bot.message_handler(commands=['kaydet'])
def kayit(message):
    kayitli = 0
    chat = message.chat.id
    markupp = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)
    buton1 = types.KeyboardButton('Yeni Kanal Ekle')
    buton2 = types.KeyboardButton('iptal')
    buton3 = types.KeyboardButton('Kanal Sil')
    markupp.add(buton1, buton2, buton3)

    if not chat == sahip:
        bot.send_message(chat, "Bu komut şuan bakımda!")
        return
    if chat in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    bina = collection.find_one({"_id": chat})
    try:
        for chan in bina['kanal']:
            try:
                kbilgi = bot.get_chat(chan)
                print(kbilgi)
            except Exception as e:
                print(e)
                collection.update_one({"_id": user}, {"$pull": {"kanal": chan[kayitli]}})
                print("Kanal silindi")
            else:    
                bot.send_message(chat, "Kayit No: {}\n\nKanalınız: {}".format(kayitli+1, kbilgi.title))
                kayitli = kayitli + 1
    except:
        pass
    try:
        tokenn = bina['token']
    except:
        msg = bot.send_message(chat, """📝 <i>Lütfen</i> <a href="https://tr.link/member/tools/quick">burdan</a> <i>aldığınız API adresinizi gönderin</i>""", reply_markup=markup)
        bot.register_next_step_handler(msg, apikayit)
    else:
        msg = bot.send_message(chat, "API: {}\nToplam: {}".format(tokenn, kayitli), reply_markup=markupp)
        bot.register_next_step_handler(msg, kayitapi)

def kayitapi(message):
    chat = message.chat.id
    mesaj = message.text
    if mesaj.lower() == "kanal sil":
        msg = bot.send_message(chat, "Silmek istediğiniz kanalın kayıt numarasını girin.")
        bot.register_next_step_handler(msg, ksil)
        return
    if mesaj.lower() == "iptal":
        msg = bot.send_message(chat, "İptal Edildi.", reply_markup=markup)
        return
    msg = bot.send_message(chat, """📝 <i>Lütfen kanalınızdan bir gönderi iletin.</i>""", reply_markup=markup)
    bot.register_next_step_handler(msg, kanalkayit)

def ksil(message):
    mesaj = int(message.text) - 1
    user = message.from_user.id
    if not message.text.isdigit():
        bot.send_message(chat, "Lütfen geçerli bir numara verin")
        return
    chat = message.chat.id
    bul = collection.find_one({"_id": user})
    x = bul['kanal']
    try:
        collection.update_one({"_id": user}, {"$pull": {"kanal": x[mesaj]}})
    except:
        bot.send_message(chat, "Yanlış bir numara girdiniz.")
    else:
        bot.send_message(chat, "Kanalınız silindi.")

def apikayit(message):
    token = message.text
    mid = message.id
    user = message.from_user.id
    mids = mid+1
    chat = message.chat.id
    bot.send_message(chat, "<code>👁️ API adresiniz kontrol ediliyor...</code>", parse_mode='MarkDown')
    s = requests.Session()
    link = s.get("https://ay.live/api")
    cookies = dict(link.cookies)
    ket = s.get(f"https://tr.link/api/?api={token}&url=yourdestinationlink.com&format=text&alias=&ct=1", cookies=cookies).text
    print(ket)
    if ket == None:
        msg = bot.edit_message_text("""<b>✖️ Geçersiz Bir API adresi girdiniz!</b> <i>Lütfen <a href="https://tr.link/member/tools/api">bu adresen</a> yeniden alın.</i>""", chat, mids)
        bot.register_next_step_handler(msg, apikayit)
        return
    bnb = collection.find_one({"_id": user})
    key = {"_id": user, "token": token, "kanal": [], "kaynak": "1", "sablon": "2"}
    if bnb == None:
        collection.insert_one(key)
    else:
        collection.update_one({"_id": user}, {"$set": {"token": token}})
    msg = bot.edit_message_text("<b>🟢 API kaydedildi!</b>", chat, mids)
    bot.register_next_step_handler(msg, kayit)

def kanalkayit(message):
    chat = message.chat.id
    user = message.from_user.id
    kanals = []
    if not message.forward_from_chat:
        msg = bot.send_message(chat, "↪️ Bunun ne olduğu hakkında bir fikrim yok! Lütfen kanaldan herhangi bir gönderi iletin.")
        bot.register_next_step_handler(msg, kanalkayit)
        return
    kanal = message.forward_from_chat.id
    kanals.append(str(kanal))
 
    y = collection.find_one({"_id": user})
    
    collection.update_one({"_id": user}, {"$push":{"kanal": str(kanal)}})
    
    bot.reply_to(message,"<b>🟢Bilgileriniz Kaydedildi.</b>\n\n <i>Kaynak kanalını değiştirmek isterseniz /kaynak yazın.</i>")

@bot.message_handler(commands=['sablon'])
def sablonn(message):
    chat = message.chat.id
    if chat in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    
    msg = bot.send_message(chat, """<b>Şablon No:1</b>
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

Üstteki şablonlardan kullanmak isterseniz, istediğiniz şablonun numarasını gönderin.

<i>Eğer kendi şablonunuzu oluşturmak isterseniz üstteki şablonlardaki gibi</i> <b>{aciklama}</b> ve <b>{link}</b> <i>kelimelerinin bulunduğundan emin olun yoksa şablon çalışmaz</i>""", reply_markup=markup)
    bot.register_next_step_handler(msg, sabloniki)

def sabloniki(message):
    mesaj = message.text
    chat = message.chat.id
    user = message.from_user.id
    if not mesaj.isdigit():
        if mesaj.find("{link}") == -1 or mesaj.find("{aciklama}") == -1:
            msg = bot.send_message(chat, """ ❌<i> Lütfen mesajınızda "{link}" ve "{aciklama}" bulunduğudan emin olun.</i> """)
            bot.register_next_step_handler(msg, sabloniki)
            return
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
    if user in kara:
        bot.send_message(chat, "🤓 Üzgünüm senin gibi aptal birisi için çalışmıyorum")
        return
    
    msg = bot.send_message(chat, """<b>Kullanmak istediğiniz kaynak kanalınının numarasını gönderin:
    
    Kaynak No:1</b>
    <a href="https://t.me/joinchat/UYu8q0gBTUdUudDL">Link Mahzeni</a>
    
    <b>Kaynk No:2</b>
    <a href="https://t.me/joinchat/MhxcfKLh3aQ4OWU0">Bedava Link</a>

<b>❗Hepsinden atsın fütursuzca kanalımı sikmek istiyorum diyorsan 0 yaz</b>
    
    
    """, disable_web_page_preview=True, reply_markup=markup)
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
    bcount = 0
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
            if kaynak == "1" or kaynak == "0":
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
                    count = count + 1
                except Exception as e:
                    print(e)
                    print(f"Hatalı kanal: {kanal}")
                    e = str(e)
                    print(e)
                    if e.find("bot is not a member") != -1:
                        collection.delete_one({"_id": user})
                        bot.send_message(user, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                        print(f"{kanal} kayıtlardan silindi.")
                print("Başarılı!")
            else:
                pass
        bot.send_message(-1001352123979, "Link Mahzeni kanalından, {} Kanalda Foto Post Paylaşıldı.".format(count))
    if chat == -1001122395785:
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
            print(bkaynak)
            sleep(2)
            if bkaynak == "2" or bkaynak == "0":
                bjson = s.get(f"https://ay.live/api/?api={btoken}&url={bmesajb}&alias=&ct=1", cookies=cookies).json()
                blink = bjson['shortenedUrl']
                print(f"{bkanal} + {blink} + {btoken}")
                try:
                    if bsablon == "1":
                        bsablon = f"🔥{baciklama}\n\n🔱 TIKLA 👉 {blink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                    elif bsablon == "2" or bsablon == "3":
                        bsablon = f"{baciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {blink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                    else:
                        bsoll = bsablon.split("{link}")
                        bsal = bsoll[0].split("{aciklama}")
                    
                        bsablon = f"{bsal[0]}{baciklama}{bsal[1]}{blink}{bsoll[1]}"
                    sleep(1)
                    bot.send_photo(bkanal, bmedya, caption=bsablon)
                    bcount = bcount + 1
                except Exception as e:
                    print(e)
                    print(f"Hatalı kanal: {bkanal}")
                    e = str(e)
                    print(e)
                    if e.find("bot is not a member") != -1:
                        collection.delete_one({"_id": buser})
                        bot.send_message(buser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                        print(f"{bkanal} kayıtlardan silindi.")
                    
                print("Başarılı!")
        bot.send_message(-1001352123979, "Bedava Link kaynağından, {} Kanalda Foto Post Paylaşıldı.".format(bcount))

@bot.channel_post_handler(content_types=['video'])
def poster(message):
    count = 0
    bcount = 0
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
            if kaynak == "1" or kaynak == "0":
                json = s.get(f"https://ay.live/api/?api={token}&url={mesajb}&alias=&ct=1", cookies=cookies).json()
                link = json['shortenedUrl']
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
                    
                    print(f"{kanal} + {link} + {token}")
                    bot.send_video(kanal, medya, caption=sablon)
                    count = count + 1
                except Exception as e:
                    print(e)
                    print(f"Hatalı kanal: {kanal}")
                    e = str(e)
                    print(e)
                    if e.find("bot is not a member") != -1:
                        collection.delete_one({"_id": user})
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
            print(bkaynak)
            sleep(1)
            if bkaynak == "2" or bkaynak == "0":
                bjson = s.get(f"https://ay.live/api/?api={btoken}&url={bmesajb}&alias=&ct=1", cookies=cookies).json()
                blink = bjson['shortenedUrl']
                print(f"{bkanal} + {blink} + {btoken}")
                try:
                    if bsablon == "1":
                        bsablon = f"🔥{baciklama}\n\n🔱 TIKLA 👉 {blink}\n\n📛 SESİ AÇ 'a tıklamayı unutma"
                    elif bsablon == "2" or bsablon == "3":
                        bsablon = f"{baciklama} \n\n         𝙇𝙄𝙉𝙆🔗 {blink}\n\n🔔ʙɪʟᴅɪʀɪᴍʟᴇʀɪ ᴀçᴍᴀʏı ᴜɴᴜᴛᴍᴀʏıɴ.\n\n📌 Link Nasıl Açılır Bilmiyorsanız\n\n👉 @linkgec06"
                    else:
                        bsoll = bsablon.split("{link}")
                        bsal = bsoll[0].split("{aciklama}")
                    
                        bsablon = f"{bsal[0]}{baciklama}{bsal[1]}{blink}{bsoll[1]}"
                    
                    bot.send_video(bkanal, bmedya, caption=bsablon)
                    bcount = bcount + 1
                except Exception as e:
                    print(e)
                    print(f"Hatalı kanal: {bkanal}")
                    e = str(e)
                    print(e)
                    if e.find("bot is not a member") != -1:
                        collection.delete_one({"_id": buser})
                        bot.send_message(buser, "Botu kanalınızdan çıkardığınız için kanalınız silindi.")
                        print(f"{bkanal} kayıtlardan silindi.")
                    
                print("Başarılı!")
        bot.send_message(-1001352123979, "Bedava Link kanalından, {} Kanalda Video Post Paylaşıldı.".format(bcount))



bot.enable_save_next_step_handlers(delay=4)

bot.load_next_step_handlers()

bot.polling()
