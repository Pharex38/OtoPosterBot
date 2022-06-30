
from . import *

markup = ForceReply(selective=False)

    
def site_isim(no):
    if no == "0":
        return "URLcik"
    elif no == "1":
        return "TRLink"
    elif no == "2":
        return "PND.TL"
    elif no == "3":
        return "Exe.io"
    elif no == "4":
        return "Ouo.io"
    elif no == "5":
        return "Pubiza"
    elif no == "6":
        return "Gir.ist"
    elif no == "7":
        return "URLAbly"
    
    else:
        return "Bulunamadı"


def dugme(user):
    first = collection.find_one({'_id': user})
    try:
        first['token']
    except:
        return ReplyKeyboardMarkup(keyboard=[['📝 Kaydet']], row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)
    else:
        return ReplyKeyboardMarkup(keyboard=[['🖥 Kanal Menü'], ['🎛 Post Menü', '🔗 API Menü'], ['🛠 Ekstralar']], input_field_placeholder="Merhaba!", resize_keyboard=True)


def kanalmenumark():
    return ReplyKeyboardMarkup(keyboard=[['🔶 Yeni Kanal Ekle', '🗑️ Kanal Sil'], ['▶️ SFS Modu', '💠 Tür Değiştir'], ['↩️ Ana Menü']], resize_keyboard=True, selective=True)

def postmenumark():
    return ReplyKeyboardMarkup(keyboard=[['⛓️ Elle Post Paylaş', '⏱ Zamanladıklarım'], ['🔧 Kaynak', '📏 Şablon'], ['↩️ Ana Menü']], resize_keyboard=True, selective=True)

def apimenumark():
    return ReplyKeyboardMarkup(keyboard=[['♻️ API değiştir', '🔗 Site değiştir'], ['🤖 Alternatif Link'], ['↩️ Ana Menü']], resize_keyboard=True, selective=True)

def ekstralarmenumark():
    return ReplyKeyboardMarkup(keyboard=[['❤️ Beğeni Butonları', '🍎 iOS Ban Kontrol'], ['📌 Post Sabitleme'], ['🔁 Tekrarlı Post Paylaş'], ['↩️ Ana Menü']], resize_keyboard=True, selective=True)

def imark():
    imark = ReplyKeyboardMarkup(keyboard=[['❌ İptal']], one_time_keyboard=True, resize_keyboard=True, selective=True)
    return imark

async def ioskontrolmark(user):
    iosk = []
    iosc = 0
    for ikan in collection.find_one({"_id": user})['kanal']:
        try:
            ioski = await bot.get_chat(ikan).title
        except:
            continue
        iosk.append([InlineKeyboardButton(ioski, callback_data=f"iosk-{iosc}")])
        iosc += 1
    iosk.append([InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")])
    return InlineKeyboardMarkup(iosk)

def cekilismark():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Çekilişe Katıl!", callback_data="katil")]])

def tekrarlipostmark(user, context):
    silbutts = [InlineKeyboardButton("Tekrarli Post Sil", callback_data="tekrarlisil")] if len(context.job_queue.get_jobs_by_name(f"ts{user}")) != 0 else []
    return InlineKeyboardMarkup([[InlineKeyboardButton("Yeni Post Oluştur", callback_data="yenitekrarli")], silbutts, [InlineKeyboardButton("❌ İptal", callback_data="iptal")]])

def tspostmod(user):
    return InlineKeyboardMarkup([[InlineKeyboardButton("Postlardan birini rastgele paylaş.", callback_data="tsmod-rastgele")], [InlineKeyboardButton("Postları sırayla birer birer paylaş.", callback_data="tsmod-sirali")]])

def tekrarlipostsilmark(user, context):
    siltp = []
    tsjobs = context.job_queue.get_jobs_by_name(f"ts{user}")
    tsc = 0
    for stkan in tsjobs:
        siltp.append([InlineKeyboardButton(stkan.context['baslik'], callback_data="tssil-{}".format(tsc))])
        tsc += 1
    if len(tsjobs) == 0:
        siltp.append([InlineKeyboardButton("Hiç tekrarli post oluşturmamışsınız!", callback_data="iptal")])        
    siltp.append([InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")])
    return InlineKeyboardMarkup(siltp)

async def tekrarlipostkan(user, context):
    tpk = []
    for tkan in collection.find_one({"_id": user})['kanal']:
        try:
            tkanisim = await bot.get_chat(tkan).title
        except:
            continue
        if tkan in context.user_data['tskan']:
            tkanisim += " ✅"
        else:
            tkanisim += " ➕"
        tpk.append([InlineKeyboardButton(tkanisim, callback_data="tkan+{}".format(tkan))])
    tpk.append([InlineKeyboardButton("👍 Bitti", callback_data="tsenough")])
    tpk.append([InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")])
    return InlineKeyboardMarkup(tpk)

def tekrarlisaatmark():
    tsmk = []
    tsmksatir = []
    for ts in range(1, 25):
        tsmksatir.append(InlineKeyboardButton(str(ts), callback_data="ts-"+str(ts)))
        if ts % 6 == 0:
            tsmk.append(tsmksatir)
            tsmksatir = []
    tsmk.append([InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")])
    return InlineKeyboardMarkup(tsmk)

async def sfsmark(user):
    sfs_dat = collection.find_one({"_id": user})
    sfsbutno = 0
    sfskeyb = []
    sfssatir = []
    for sfskan in sfs_dat['kanal']:
        try:
            sfsname = await bot.get_chat(sfskan).title
        except:
            pass
        else:
            sfslink = "tg://privatepost?channel={}&post=9999999".format(sfskan[3:])
            sfssatir.append(InlineKeyboardButton(sfsname, url=sfslink))
            if sfskan in sfs_dat['eski']:
                sfssatir.append(InlineKeyboardButton("Açık", callback_data="sfs-{}".format(sfsbutno)))
            else:
                sfssatir.append(InlineKeyboardButton("Kapalı", callback_data="sfs-{}".format(sfsbutno)))
            sfskeyb.append(sfssatir)
            sfssatir = []
        sfsbutno += 1
    return InlineKeyboardMarkup(sfskeyb)

async def pinmark(user):
    pin_dat = collection.find_one({"_id": user})
    pinbutno = 0
    pinkeyb = []
    pinsatir = []
    for pinkan in pin_dat['kanal']:
        try:
            pinname = await bot.get_chat(pinkan).title
        except:
            pass
        else:
            pinlink = "tg://privatepost?channel={}&post=9999999".format(pinkan[3:])
            pinsatir.append(InlineKeyboardButton(pinname, url=pinlink))
            if pinkan in pin_dat['pin']:
                pinsatir.append(InlineKeyboardButton("Açık", callback_data="pin-{}".format(pinbutno)))
            else:
                pinsatir.append(InlineKeyboardButton("Kapalı", callback_data="pin-{}".format(pinbutno)))
            pinkeyb.append(pinsatir)
            pinsatir = []
        pinbutno += 1
    return InlineKeyboardMarkup(pinkeyb)

def miktarliistekmark(miktarikan, sayi):
    return InlineKeyboardMarkup([[InlineKeyboardButton(f"Onayla ⏩⏩ {sayi}", callback_data="isteklink-{}-{}-all".format(miktarikan, sayi))], [InlineKeyboardButton("-100", callback_data="miktari-{}-{}".format(miktarikan, sayi-100)), InlineKeyboardButton("-10", callback_data="miktari-{}-{}".format(miktarikan, sayi-10)),  InlineKeyboardButton("+10", callback_data="miktari-{}-{}".format(miktarikan, sayi+10)), InlineKeyboardButton("+100", callback_data="miktari-{}-{}".format(miktarikan, sayi+100))]])

async def istekmark(user):
    istek_dat = collection.find_one({"_id": user})
    istekbutno = 0
    istekkeyb = []
    isteksatir = []
    isteksatir2 = []
    for istekkan in istek_dat['kanal']:
        try:
            istekname = await bot.get_chat(istekkan).title
        except:
            pass
        else:
            isteklink = "tg://privatepost?channel={}&post=9999999".format(istekkan[3:])
            isteksatir.append(InlineKeyboardButton(istekname, url=isteklink))
            if istekkan in collection.find_one({"_id": 0})['istek']:
                isteksatir2.append(InlineKeyboardButton("✅", callback_data="istek-{}".format(istekbutno)))
            else:
                isteksatir2.append(InlineKeyboardButton("⚫", callback_data="istek-{}".format(istekbutno)))
            isteksatir2.append(InlineKeyboardButton(f"♐", callback_data="isteklink-{}-99999".format(istekbutno)))
            isteksatir2.append(InlineKeyboardButton(f"🔢", callback_data="smiktari-{}".format(istekbutno)))
            if len(isteksatir) == 2:
                istekkeyb.append(isteksatir)
                istekkeyb.append(isteksatir2)
                isteksatir = []
                isteksatir2 = []
            
        istekbutno += 1
    if len(isteksatir) != 0:
        istekkeyb.append(isteksatir)
        istekkeyb.append(isteksatir2)
    return InlineKeyboardMarkup(istekkeyb)

def dagme():
    dagme = ReplyKeyboardMarkup(keyboard=[['📝 Kaydet']], row_width=2, one_time_keyboard=True, resize_keyboard=False, selective=True)
    return dagme

def sitemarkup():
    skey = []
    smark = InlineKeyboardMarkup([[InlineKeyboardButton("TRLink", callback_data="site-1")], [InlineKeyboardButton("PND.TL", callback_data="site-2")], [InlineKeyboardButton("Exe.io", callback_data="site-3")], [InlineKeyboardButton("Ouo.io", callback_data="site-4")], [InlineKeyboardButton("Pubiza", callback_data="site-5")], [InlineKeyboardButton("Gir.ist", callback_data="site-6")], [InlineKeyboardButton("URLcik", callback_data="site-0")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]])
    return smark

def altsitemarkup(asite):
    asmark = InlineKeyboardMarkup([[InlineKeyboardButton("TRLink", callback_data=f"{asite}-1")], [InlineKeyboardButton("PND.TL", callback_data=f"{asite}-2")], [InlineKeyboardButton("Exe.io", callback_data=f"{asite}-3")], [InlineKeyboardButton("Ouo.io", callback_data=f"{asite}-4")], [InlineKeyboardButton("Pubiza", callback_data=f"{asite}-5")], [InlineKeyboardButton("Gir.ist", callback_data=f"{asite}-6")], [InlineKeyboardButton("URLcik", callback_data=f"{asite}-0")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]])
    return asmark

def altmarkup(user):

    altkey = [[InlineKeyboardButton("Sıralı", callback_data="sistem-2")], [InlineKeyboardButton("Tek Post İki Link", callback_data="sistem-1")], [InlineKeyboardButton("Gelişmiş", callback_data="sistem-gelismis")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]]
    if collection.find_one({"_id": user})['altapi'] != "None":
        altkey.append([InlineKeyboardButton("⛔ Alternatif Kaldır", callback_data="akaldır")])
    altmark = InlineKeyboardMarkup(altkey)
    return altmark

def inmark():
    inmark = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
    return inmark

def ozelmark():
    omark = InlineKeyboardMarkup([[InlineKeyboardButton("➕ Oluştur ➕", callback_data="okayt")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
    return omark

async def icerikmark(user):
    icerik_dat = collection.find_one({"_id": user})
    icerikbutno = 0
    icerikkeyb = []
    iceriksatir = []
    for icerikkan in icerik_dat['kanal']:
        try:
            icerikname = await bot.get_chat(icerikkan).title
        except:
            pass
        else:
            iceriklink = "tg://privatepost?channel={}&post=9999999".format(icerikkan[3:])
            iceriksatir.append(InlineKeyboardButton(icerikname, url=iceriklink))
            if icerikkan in icerik_dat['icerik']:
                iceriksatir.append(InlineKeyboardButton("Arşiv", callback_data="icerik-{}-m".format(icerikbutno)))
            else:
                iceriksatir.append(InlineKeyboardButton("+18", callback_data="icerik-{}-m".format(icerikbutno)))
            icerikkeyb.append(iceriksatir)
            iceriksatir = []
        icerikbutno += 1
    return InlineKeyboardMarkup(icerikkeyb)

async def okaykanalmark(user):
    okayk_dat = collection.find_one({"_id": user})
    for okz in OzelCol.find():
        if user in okz['kanal']:
            okaynakk = okz
            break
    okaykbutno = 0
    okaykkeyb = []
    okayksatir = []
    for okaykkan in okayk_dat['kanal']:
        try:
            okaykname = await bot.get_chat(okaykkan).title
        except:
            pass
        else:
            okayklink = "tg://privatepost?channel={}&post=9999999".format(okaykkan[3:])
            okayksatir.append(InlineKeyboardButton(okaykname, url=okayklink))
            if okaykkan in okaynakk['kaynak']:
                okayksatir.append(InlineKeyboardButton("✅", callback_data="okayk-{}".format(okaykbutno)))
            else:
                okayksatir.append(InlineKeyboardButton("⚫", callback_data="okayk-{}".format(okaykbutno)))
            okaykkeyb.append(okayksatir)
            okayksatir = []
        okaykbutno += 1
    return InlineKeyboardMarkup(okaykkeyb)

def ozelkaynakmark(user, kanil):
    y = OzelCol.find_one({"kanal": {"$in": [user]}})
    y = y['_id'] if y else "yok"
    if user == y:
        if OzelCol.find_one({"_id": y})['icerik'] == "arsiv":
            ozicerik = {"isim": "🗃️ Arşiv 🗃️", "data": "ozicerik-arsiv"}
        else:
            ozicerik = {"isim": "🔞 +18 🔞", "data": "ozicerik-+18"}
        if OzelCol.find_one({"_id": user})["log"] == "yok":
            kmark = InlineKeyboardMarkup([[InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk")], [InlineKeyboardButton("🤖 Botlog Oluştur 🤖", callback_data="logokay")], [InlineKeyboardButton("🌐 Bağlı Kanallarım 🌐", callback_data="okaykanal")], [InlineKeyboardButton("💣 Kaynağı Yok Et 💣", callback_data="eminmisin")], [InlineKeyboardButton("Kaynak Tür: "+ozicerik['isim'], callback_data=ozicerik['data'])], [InlineKeyboardButton("🔧 Ana Kaynaklar 🔧", callback_data="anakay")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
        else:
            kmark = InlineKeyboardMarkup([[InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk")], [InlineKeyboardButton("🤖 Botlog Kaldır ❌", callback_data="logokaldir")], [InlineKeyboardButton("🌐 Bağlı Kanallarım 🌐", callback_data="okaykanal")], [InlineKeyboardButton("💣 Kaynağı Yok Et 💣", callback_data="eminmisin")], [InlineKeyboardButton("Kaynak Tür: "+ozicerik['isim'], callback_data=ozicerik['data'])], [InlineKeyboardButton("🔧 Ana Kaynaklar 🔧", callback_data="anakay")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
    else:
        kmark = InlineKeyboardMarkup([[InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk")], [InlineKeyboardButton("🌐 Bağlı Kanallarım 🌐", callback_data="okaykanal")], [InlineKeyboardButton("🔧 Ana Kaynaklar 🔧", callback_data="anakay")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
    return kmark 
    

async def kaynakmark(user, kanil):
    u = collection.find_one({"_id": user})
    linkkaynakkeyb = []
    butonkaynakkeyb = []
    anakaynakkeyb = []
    for kaynak in KaynakCol.find({}):
        if kaynak['no'] in ignorekaynak:
            continue
        if kaynak['icerik'] == "arsiv" and not u['kanal'][int(kanil)] in u['icerik']:
            continue
        
        if kaynak['icerik'] != "arsiv" and u['kanal'][int(kanil)] in u['icerik']:
            continue
        try:
            getkaynak = await bot.get_chat(kaynak["_id"])
        except:
            k_title = "𝙺𝚊𝚢𝚗𝚊ğ𝚊 𝚞𝚕𝚊şı𝚕𝚊𝚖ı𝚢𝚘𝚛."
            k_link = "https://t.me/otoposterbotlog"
        else:
            k_title = getkaynak.title
            k_link = getkaynak.invite_link
        if k_link == None:
            k_link = "tg://privatepost?channel={}&post=9999999".format(str(kaynak['_id'])[3:])
        saatbut = InlineKeyboardButton("⏳", callback_data="zaman-{}".format(kaynak['sahip']))
        if user in kaynak['kaynak'] and u['kanal'][int(kanil)] in kaynak['kanal']:
            kb1 = InlineKeyboardButton("✅", callback_data="kaynak-{}-{}".format(kaynak['sahip'], kanil))
        else:
            kb1 = InlineKeyboardButton("⚫", callback_data="kaynak-{}-{}".format(kaynak['sahip'], kanil))
        butonkaynakkeyb.append(kb1)
        butonkaynakkeyb.append(saatbut)
        linkkaynakkeyb.append(InlineKeyboardButton("{}".format(k_title), url="{}".format(k_link)))
        if len(linkkaynakkeyb) == 2:
            anakaynakkeyb.append(linkkaynakkeyb)
            anakaynakkeyb.append(butonkaynakkeyb)
            linkkaynakkeyb = []
            butonkaynakkeyb = []
    if not len(linkkaynakkeyb) == 0:
        anakaynakkeyb.append(linkkaynakkeyb)
        anakaynakkeyb.append(butonkaynakkeyb)
    if len(u['kanal']) == 1:
        pass
    elif kanil == len(u['kanal'])-1:
        anakaynakkeyb.append([InlineKeyboardButton("⏪Önceki Kanal⏪", callback_data="solyan-{}".format(kanil))])
    elif kanil == 0:
        anakaynakkeyb.append([InlineKeyboardButton("⏩Sonraki Kanal⏩", callback_data="sagyan-{}".format(kanil))])
    else:
        anakaynakkeyb.append([InlineKeyboardButton("⏪Önceki Kanal⏪", callback_data="solyan-{}".format(kanil)), InlineKeyboardButton("⏩Sonraki Kanal⏩", callback_data="sagyan-{}".format(kanil))])
    if u['kanal'][int(kanil)] in u['icerik']:
        turtext = "Arşiv"
    else:
        turtext = "+18"
    anakaynakkeyb.append([InlineKeyboardButton("💠 Tür Değiştir: "+turtext, callback_data="icerik-{}-k".format(kanil))])
    if u['ozel']:
        anakaynakkeyb.append([InlineKeyboardButton("♋️ Özel Kaynak Ayarları 🛠", callback_data="ozayar")])
    else:
        anakaynakkeyb.append([InlineKeyboardButton("♋️ Özel Kaynak Oluştur ♋️", callback_data="okay")])
    anakaynakkeyb.append([InlineKeyboardButton("❌ Menüyü Kapat ❌", callback_data="aiptal")])
    kmark = InlineKeyboardMarkup(inline_keyboard=anakaynakkeyb)
    return kmark

def ekmark():
    ekkeyb = [[InlineKeyboardButton("Kur", callback_data="ekkur")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]]
    return InlineKeyboardMarkup(inline_keyboard=ekkeyb)

def zamanmenumark(user):
    if collection.find_one({"_id": user})['vakit'] == 0:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("Post Zamanları Ayarla", callback_data="pzayarla")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("Post Zamanları Ayarla", callback_data="pzayarla")], [InlineKeyboardButton("Post Zamanlarını Devre Dışı Bırak", callback_data="pzkaldır")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]])

def advaltmark(user):
    advkeyb = []
    advdat = collection.find_one({"_id": user})
    advkeyb.append([InlineKeyboardButton("Sistem: Tek Link" if advdat['altsite'] == "sirali" else "Sistem: Çift Link", callback_data=f"advsistem"), InlineKeyboardButton("ℹ️ Bilgi", callback_data="advbilgi")])
    for advdex, advalt in enumerate(advdat['altapi']):
        advisim = site_isim(advalt["site"])
        advkeyb.append([InlineKeyboardButton(advisim, callback_data=f"advalt-{advdex}"), InlineKeyboardButton("API 👁️", callback_data=f"advapi-{advdex}"), InlineKeyboardButton("⛔ Kaldır", callback_data=f"advsil-{advdex}")])
    advkeyb.append([InlineKeyboardButton("➕ Ekle", callback_data="advekle"), InlineKeyboardButton("⛔ Tümünü Kaldır", callback_data="akaldır")])
    return InlineKeyboardMarkup(advkeyb)

def sablonmark(user):
    if collection.find_one({"_id": user})['sablon'] in ["1", "2", "3", "9"]:
        buts = InlineKeyboardButton("➕ Şablon Oluştur ➕", callback_data="sablon")
        samark = InlineKeyboardMarkup(inline_keyboard=[[buts]], row_width=2)
        return samark
    else:
        buts = InlineKeyboardButton("➕ Şablon Değiştir ➕", callback_data="sablon")
        buts2 = InlineKeyboardButton("🔁 Varsayılan Şablonu Kullan 🔁", callback_data="vsablon")
        buts3 = InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")
        samark = InlineKeyboardMarkup(inline_keyboard=[[buts], [buts2], [buts3]], row_width=2)
        return samark

async def patmark(user):
    zero = 0
    pkeyb = [[InlineKeyboardButton("💎Hepsine Gönder💎", callback_data="pat-0")]]
    pkul = collection.find_one({"_id": user})

    for k in pkul['kanal']:
        try:
            kn = await bot.get_chat(k)
            kis = kn.title
        except:
            kis = "Kanala ulaşılamadı."
        zero += 1
        pkeyb.append([InlineKeyboardButton("{}".format(kis), callback_data="pat-{}".format(zero))])
    pkeyb.append([InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")])

    pmark = InlineKeyboardMarkup(pkeyb)
    return pmark
    
async def gen_markup(user):
    keyb = []
    kayd = collection.find_one({"_id": user})
    butonno = 0
    for k in kayd['kanal']:
        try:
            ismi = await bot.get_chat(k)
        except:
            collection.update_one({"_id": user}, {"$pull": {"kanal": k}})
        else:
            keyb.append([InlineKeyboardButton("{}".format(ismi.title), callback_data="sil-{}".format(butonno))])
            butonno += 1
    keyb.append([InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")])
    silkey = InlineKeyboardMarkup(keyb)
    
    return silkey

def begenimark(eudat):
    if len(eudat['begeni']) < 1:
        bmark = InlineKeyboardMarkup([[InlineKeyboardButton('Beğeni Butonları Oluştur.', callback_data="begeniolustur")], [InlineKeyboardButton('İptal.', callback_data="iptal")]])
    else:
        bmark = InlineKeyboardMarkup([[InlineKeyboardButton('Butonları değiştir.', callback_data="begeniolustur")], [InlineKeyboardButton('Butonları kaldır', callback_data="begenikaldir")], [InlineKeyboardButton('İptal.', callback_data="iptal")]])
    return bmark

def jobmark(user, context):
    jobs = context.job_queue.get_jobs_by_name(str(user))
    jobkeyb = []
    jcount = 0
    for jop in jobs:
        if jop.name.startswith(str(user)):
            jobstr = str(jop.job)
            jnam = jobstr.find("date[")
            jname = jobstr[jnam+5:jnam+25]
            jobkeyb.append([InlineKeyboardButton(jname, callback_data="jop-{}".format(jcount))])
        jcount += 1
    jobkeyb.append([InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")])
    if jcount == 0:
        jobkeyb.append([InlineKeyboardButton("Henüz bir post zamanlamamışsınız.", callback_data="iptal")])
    return InlineKeyboardMarkup(jobkeyb)

def panelkaynakmark(user):
    return InlineKeyboardMarkup([[InlineKeyboardButton("🆕 Son Güncellemeler", callback_data="panelguncellemeler")], [InlineKeyboardButton("🌐 Kullanan Kanallar", callback_data="panelkanal".format(user))], [InlineKeyboardButton("👥 Kullanan Kişiler", callback_data="panelkullanici")], [InlineKeyboardButton("⌛ Zaman Butonunun Mesajını Değiştir", callback_data="panelzaman")], [InlineKeyboardButton("⛔️ Kaynak kuralları", callback_data="panelkural")]])

def yenikaynakmark(user):
    return InlineKeyboardMarkup([[InlineKeyboardButton("")]])

def ayarlarmark():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("s", callback_data="panelguncellemeler")],
    ])

def eminmisin():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Evet, kesinlikle eminim.", callback_data="yoket")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
    