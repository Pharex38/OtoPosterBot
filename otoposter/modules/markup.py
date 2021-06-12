from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton


def sitemarkup():
    skey = []
    smark = InlineKeyboardMarkup([[InlineKeyboardButton("TRLink", callback_data="site-1")], [InlineKeyboardButton("PND.TL", callback_data="site-2")], [InlineKeyboardButton("Exe.io", callback_data="site-3")], [InlineKeyboardButton("Ouo.io", callback_data="site-4")], [InlineKeyboardButton("Pubiza", callback_data="site-5")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]])
    return smark

def altsitemarkup(sss):
    asmark = InlineKeyboardMarkup([[InlineKeyboardButton("TRLink", callback_data="asite-1-{}".format(sss))], [InlineKeyboardButton("PND.TL", callback_data="asite-2-{}".format(sss))], [InlineKeyboardButton("Exe.io", callback_data="asite-3-{}".format(sss))], [InlineKeyboardButton("Ouo.io", callback_data="asite-4-{}".format(sss))], [InlineKeyboardButton("Pubiza", callback_data="asite-5-{}".format(sss))], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]])

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

def kaynakmark(user):
    u = collection.find_one({"_id": user})
    saatbut = InlineKeyboardButton("⏳", callback_data="zaman-1")
    bsaatbut = InlineKeyboardButton("⏳", callback_data="zaman-2")
    csaatbut = InlineKeyboardButton("⏳", callback_data="zaman-3")
    dsaatbut = InlineKeyboardButton("⏳", callback_data="zaman-4")
    esaatbut = InlineKeyboardButton("⏳", callback_data="zaman-5")
    fsaatbut = InlineKeyboardButton("⏳", callback_data="zaman-6")
    gsaatbut = InlineKeyboardButton("⏳", callback_data="zaman-7")
    
    ubut =InlineKeyboardButton("{}".format(mahzen.title), url="{}".format(mahzen.invite_link))
    bbut =InlineKeyboardButton("{}".format(bedava.title), url="{}".format(bedava.invite_link))
    cbut =InlineKeyboardButton("{}".format(evi.title), url="{}".format(evi.invite_link))
    dbut =InlineKeyboardButton("{}".format(bashub.title), url="{}".format(bashub.invite_link))
    ebut =InlineKeyboardButton("{}".format(acikmi.title), url="{}".format(acikmi.invite_link))
    fbut =InlineKeyboardButton("{}".format(tutan.title), url="{}".format(tutan.invite_link))
    gbut =InlineKeyboardButton("{}".format(muho.title), url="{}".format(muho.invite_link))
    if u['ozel']:
        for x in OzelCol.find({}):
            if user in x['kanal']:
                y = x['_id']
        if user == y:
            if OzelCol.find_one({"_id": user})["log"] == "yok":
                kmark = InlineKeyboardMarkup([[InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk")], [InlineKeyboardButton("🤖 Botlog Oluştur 🤖", callback_data="logokay")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
            else:
                kmark = InlineKeyboardMarkup([[InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk")], [InlineKeyboardButton("🤖 Botlog Kaldır ❌", callback_data="logokaldir")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
        else:
            kmark = InlineKeyboardMarkup([[InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
        return kmark        

    if "1" in u['kaynak']:
        kb1 = InlineKeyboardButton("✅", callback_data="kaynak-1")
    else:
        kb1 = InlineKeyboardButton("⚫", callback_data="kaynak-1")
    if "2" in u['kaynak']:
        kb2 = InlineKeyboardButton("✅", callback_data="kaynak-2")
    else:
        kb2 = InlineKeyboardButton("⚫", callback_data="kaynak-2")
    if "3" in u['kaynak']:
        kb3 = InlineKeyboardButton("✅", callback_data="kaynak-3")
    else:
        kb3 = InlineKeyboardButton("⚫", callback_data="kaynak-3")
    if "4" in u['kaynak']:
        kb4 = InlineKeyboardButton("✅", callback_data="kaynak-4")
    else:
        kb4 = InlineKeyboardButton("⚫", callback_data="kaynak-4")
    if "5" in u['kaynak']:
        kb5 = InlineKeyboardButton("✅", callback_data="kaynak-5")
    else:
        kb5 = InlineKeyboardButton("⚫", callback_data="kaynak-5")
    if "6" in u['kaynak']:
        kb6 = InlineKeyboardButton("✅", callback_data="kaynak-6")
    else:
        kb6 = InlineKeyboardButton("⚫", callback_data="kaynak-6")
    if "7" in u['kaynak']:
        kb7 = InlineKeyboardButton("✅", callback_data="kaynak-7")
    else:
        kb7 = InlineKeyboardButton("⚫", callback_data="kaynak-7")
    
    kmark = InlineKeyboardMarkup(inline_keyboard=[[ubut], [kb1, saatbut], [bbut], [kb2, bsaatbut], [cbut], [kb3, csaatbut], [dbut], [kb4, dsaatbut], [ebut], [kb5, esaatbut], [gbut], [kb6, gsaatbut], [fbut], [kb7, fsaatbut], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")], [InlineKeyboardButton("♋️ Özel Kaynak Oluştur ♋️", callback_data="okay")]])
    
    return kmark

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

