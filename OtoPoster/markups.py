from .misc import *
from . import *

markup = ForceReply(selective=False)

def dugme(user):
    first = collection.find_one({'_id': user})
    if first == None:
        return ReplyKeyboardMarkup(keyboard=[['📝 Kaydet']], row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)

    dugme = ReplyKeyboardMarkup(keyboard=[['🖥 Kanal Menü'], ['🎛 Post Menü', '🔗 API Menü'], ['🛠 Ekstralar'], ['🥰 Bağış']], resize_keyboard=True)
    
    return dugme

def kanalmenumark():
    return ReplyKeyboardMarkup(keyboard=[['🔶 Yeni Kanal Ekle', '🗑️ Kanal Sil'], ['▶️ SFS Modu'], ['↩️ Ana Menü']], resize_keyboard=True, selective=True)

def postmenumark():
    return ReplyKeyboardMarkup(keyboard=[['⛓️ Elle Post Paylaş', '⏱ Zamanladıklarım'], ['🔧 Kaynak', '📏 Şablon'], ['↩️ Ana Menü']], resize_keyboard=True, selective=True)

def apimenumark():
    return ReplyKeyboardMarkup(keyboard=[['♻️ API değiştir', '🔗 Site değiştir'], ['🤖 Alternatif Link'], ['↩️ Ana Menü']], resize_keyboard=True, selective=True)

def ekstralarmenumark():
    return ReplyKeyboardMarkup(keyboard=[['❤️ Beğeni Butonları'], ['📌 Post Sabitleme', '🍎 iOS Ban Kontrol'], ['🔁 Tekrarlı Post Paylaş'], ['↩️ Ana Menü']], resize_keyboard=True, selective=True)

def imark():
    imark = ReplyKeyboardMarkup(keyboard=[['❌ İptal']], one_time_keyboard=True, resize_keyboard=True, selective=True)
    return imark

def ioskontrolmark(user):
    iosk = []
    iosc = 0
    for ikan in collection.find_one({"_id": user})['kanal']:
        try:
            ioski = bot.get_chat(ikan).title
        except:
            continue
        iosk.append([InlineKeyboardButton(ioski, callback_data=f"iosk-{iosc}")])
        iosc += 1
    iosk.append([InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")])
    return InlineKeyboardMarkup(iosk)

def cekilismark():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Çekilişe Katıl!", callback_data="katil")]])

def tekrarlipostmark():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Yeni Post Oluştur", callback_data="yenitekrarli")], [InlineKeyboardButton("Tekrarli Post Sil", callback_data="tekrarlisil")], [InlineKeyboardButton("❌ İptal", callback_data="iptal")]])

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

def tekrarlipostkan(user):
    tpk = []
    for tkan in collection.find_one({"_id": user})['kanal']:
        try:
            tkanisim = bot.get_chat(tkan).title
        except:
            continue
        tpk.append([InlineKeyboardButton(tkanisim, callback_data="tkan+{}".format(tkan))])
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

def sfsmark(user):
    sfs_dat = collection.find_one({"_id": user})
    sfsbutno = 0
    sfskeyb = []
    sfssatir = []
    for sfskan in sfs_dat['kanal']:
        try:
            sfsname = bot.get_chat(sfskan).title
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

def pinmark(user):
    pin_dat = collection.find_one({"_id": user})
    pinbutno = 0
    pinkeyb = []
    pinsatir = []
    for pinkan in pin_dat['kanal']:
        try:
            pinname = bot.get_chat(pinkan).title
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

def dagme():
    dagme = ReplyKeyboardMarkup(keyboard=[['📝 Kaydet']], row_width=2, one_time_keyboard=True, resize_keyboard=False, selective=True)
    return dagme

def sitemarkup():
    skey = []
    smark = InlineKeyboardMarkup([[InlineKeyboardButton("TRLink", callback_data="site-1")], [InlineKeyboardButton("PND.TL", callback_data="site-2")], [InlineKeyboardButton("Exe.io", callback_data="site-3")], [InlineKeyboardButton("Ouo.io", callback_data="site-4")], [InlineKeyboardButton("Pubiza", callback_data="site-5")], [InlineKeyboardButton("Gir.ist", callback_data="site-6")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]])
    return smark

def altsitemarkup():
    asmark = InlineKeyboardMarkup([[InlineKeyboardButton("TRLink", callback_data="asite-1")], [InlineKeyboardButton("PND.TL", callback_data="asite-2")], [InlineKeyboardButton("Exe.io", callback_data="asite-3")], [InlineKeyboardButton("Ouo.io", callback_data="asite-4")], [InlineKeyboardButton("Pubiza", callback_data="asite-5")], [InlineKeyboardButton("Gir.ist", callback_data="asite-6")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]])
    return asmark

def altmarkup(user):

    altkey = [[InlineKeyboardButton("Sıralı", callback_data="sistem-2")], [InlineKeyboardButton("Tek Post İki Link", callback_data="sistem-1")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]]
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

def kaynakmark(user, kanil):
    u = collection.find_one({"_id": user})
    if u['ozel']:
        for x in OzelCol.find({}):
            if user in x['kanal']:
                y = x['_id']
        if user == y:
            if OzelCol.find_one({"_id": user})["log"] == "yok":
                kmark = InlineKeyboardMarkup([[InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk")], [InlineKeyboardButton("🤖 Botlog Oluştur 🤖", callback_data="logokay")], [InlineKeyboardButton("💣 Kaynağı Yok Et 💣", callback_data="eminmisin")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
            else:
                kmark = InlineKeyboardMarkup([[InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk")], [InlineKeyboardButton("🤖 Botlog Kaldır ❌", callback_data="logokaldir")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
        else:
            kmark = InlineKeyboardMarkup([[InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
        return kmark 
    linkkaynakkeyb = []
    butonkaynakkeyb = []
    anakaynakkeyb = []
    for kaynak in KaynakCol.find({}):
        if kaynak['no'] in ignorekaynak:
            continue
        try:
            getkaynak = bot.get_chat(kaynak["_id"])
        except:
            k_title = "𝙺𝚊𝚢𝚗𝚊ğ𝚊 𝚞𝚕𝚊şı𝚕𝚊𝚖ı𝚢𝚘𝚛."
            k_link = "https://t.me/otoposterbotlog"
        else:
            k_title = getkaynak.title
            k_link = getkaynak.invite_link
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
    if len(u['kanal']) == 1:
        pass
    elif kanil == len(u['kanal'])-1:
        anakaynakkeyb.append([InlineKeyboardButton("⏪⏪", callback_data="solyan-{}".format(kanil))])
    elif kanil == 0:
        anakaynakkeyb.append([InlineKeyboardButton("⏩⏩", callback_data="sagyan-{}".format(kanil))])
    else:
        anakaynakkeyb.append([InlineKeyboardButton("⏪⏪", callback_data="solyan-{}".format(kanil)), InlineKeyboardButton("⏩⏩", callback_data="sagyan-{}".format(kanil))])
    anakaynakkeyb.append([InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")])
    anakaynakkeyb.append([InlineKeyboardButton("♋️ Özel Kaynak Oluştur ♋️", callback_data="okay")])
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

def patmark(user):
    zero = 0
    pkeyb = [[InlineKeyboardButton("Hepsine Gönder", callback_data="pat-0")]]
    pkul = collection.find_one({"_id": user})

    for k in pkul['kanal']:
        try:
            kn = bot.get_chat(k)
            kis = kn.title
        except:
            kis = "Kanala ulaşılamadı."
        zero += 1
        pkeyb.append([InlineKeyboardButton("{}".format(kis), callback_data="pat-{}".format(zero))])
    pkeyb.append([InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")])

    pmark = InlineKeyboardMarkup(pkeyb)
    return pmark
    
def gen_markup(user):
    keyb = []
    kayd = collection.find_one({"_id": user})
    butonno = 0
    for k in kayd['kanal']:
        try:
            ismi = bot.get_chat(k)
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

def eminmisin():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Evet, kesinlikle eminim.", callback_data="yoket")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
    