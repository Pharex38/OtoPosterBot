from . import *
from .misc import *

markup = ForceReply(selective=False)

def dugme(user):
    first = collection.find_one({'_id': user})
    if first == None:
        return ReplyKeyboardMarkup(keyboard=[['📝 Kaydet']], row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)

    dugme = ReplyKeyboardMarkup(keyboard=[['🖥 Kanal Menü'], ['🎛 Post Menü', '🔗 API Menü'], ['🥰 Bağış']], resize_keyboard=True)
    
    return dugme

def kanalmenumark():
    return ReplyKeyboardMarkup(keyboard=[['🔶 Yeni Kanal Ekle', '🗑️ Kanal Sil'], ['▶️ SFS Modu'], ['↩️ Ana Menü']], resize_keyboard=True, selective=True)

def postmenumark():
    return ReplyKeyboardMarkup(keyboard=[['⛓️ Elle Post Paylaş', '⏱ Zamanladıklarım'], ['🔧 Kaynak', '📏 Şablon'], ['↩️ Ana Menü']], resize_keyboard=True, selective=True)

def apimenumark():
    return ReplyKeyboardMarkup(keyboard=[['♻️ API değiştir', '🔗 Site değiştir'], ['🤖 Alternatif Link'], ['↩️ Ana Menü']], resize_keyboard=True, selective=True)

def markupp():
    markupp = ReplyKeyboardMarkup(keyboard=[['🔶 Yeni Kanal Ekle', '🗑️ Kanal Sil'], ['♻️ API değiştir', '🔗 Site değiştir'], ['⏱ Post Zamanları', '🤖 Alternatif Ekle'], ['↩️ Ana Menü']], row_width=2, one_time_keyboard=False, resize_keyboard=True)

    return markupp

def imark():
    imark = ReplyKeyboardMarkup(keyboard=[['❌ İptal']], one_time_keyboard=True, resize_keyboard=True, selective=True)

    return imark

def dagme():
    dagme = ReplyKeyboardMarkup(keyboard=[['📝 Kaydet']], row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)

    return dagme

def sitemarkup():
    skey = []
    smark = InlineKeyboardMarkup([[InlineKeyboardButton("TRLink", callback_data="site-1")], [InlineKeyboardButton("PND.TL", callback_data="site-2")], [InlineKeyboardButton("Exe.io", callback_data="site-3")], [InlineKeyboardButton("Ouo.io", callback_data="site-4")], [InlineKeyboardButton("Pubiza", callback_data="site-5")], [InlineKeyboardButton("Gir.ist", callback_data="site-6")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]])
    return smark

def altsitemarkup():
    asmark = InlineKeyboardMarkup([[InlineKeyboardButton("TRLink", callback_data="asite-1")], [InlineKeyboardButton("PND.TL", callback_data="asite-2")], [InlineKeyboardButton("Exe.io", callback_data="asite-3")], [InlineKeyboardButton("Ouo.io", callback_data="asite-4")], [InlineKeyboardButton("Pubiza", callback_data="asite-5-")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]])

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
    anakaynakkeyb = [[InlineKeyboardButton("⏪⏪", callback_data="solyan-{}".format(kanil)), InlineKeyboardButton("⏩⏩", callback_data="sagyan-{}".format(kanil))]]
    if kanil == len(u['kanal'])-1:
        anakaynakkeyb = [[InlineKeyboardButton("⏪⏪", callback_data="solyan-{}".format(kanil))]]
    elif kanil == 0:
        anakaynakkeyb = [[InlineKeyboardButton("⏩⏩", callback_data="sagyan-{}".format(kanil))]]
    if len(u['kanal']) == 1:
        anakaynakkeyb = []
   
    for kaynak in KaynakCol.find({}):
        try:
            getkaynak = bot.get_chat(kaynak["_id"])
        except:
            k_title = "Kaynağa ulaşılamıyor."
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
        kn = bot.get_chat(k)
        zero += 1
        pkeyb.append([InlineKeyboardButton("{}".format(kn.title), callback_data="pat-{}".format(zero))])
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
        except BadRequest as bd:
            if bd.args == "Chat is not found":
                raise Unauthorized
            else:
                logger.error(bd)
        except Unauthorized:
            collection.update_one({"_id": user}, {"$pull": {"kanal": k}})
        else:
            keyb.append([InlineKeyboardButton("{}".format(ismi.title), callback_data="sil-{}".format(butonno))])
            butonno += 1
    keyb.append([InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")])
    silkey = InlineKeyboardMarkup(keyb)
    
    return silkey

def begenimark(kalp, bomb, rose):
    bmark = InlineKeyboardMarkup([[InlineKeyboardButton(f"♥️{kalp}", callback_data="emo-{}-{}-{}-1".format(kalp, bomb, rose)), InlineKeyboardButton(f"💣{bomb}", callback_data="emo-{}-{}-{}-2".format(kalp, bomb, rose)), InlineKeyboardButton(f"🌹{rose}", callback_data="emo-{}-{}-{}-3".format(kalp, bomb, rose))]])
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
    