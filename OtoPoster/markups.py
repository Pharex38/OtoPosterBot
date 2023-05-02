from . import *

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
        return "Urlcik.XYZ"
    elif no == "8":
        return "Cuty.io"
    elif no == "9":
        return "ShrtFly"
    elif no == "10":
        return "Za.gl"
    elif no == "11":
        return "Link Perisi"
    elif no == "12":
        return "Linkimm.xyz"
    elif no == "13":
        return "kiw.app"
    else:
        return "Bulunamadı"

markup = ForceReply(selective=False)



def dugme(user):
    first = collection.find_one({'_id': user})
    try:
        first['token']
    except:
        return ReplyKeyboardMarkup(keyboard=[['📝 Kaydet']], row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)
    else:
        return ReplyKeyboardMarkup(keyboard=[['🖥 Kanal Menü'], ['🎛 Post Menü', '🔗 API Menü'], ['🛠 Ekstralar']], input_field_placeholder="Merhaba!", resize_keyboard=True)


def kanalmenumark(user):
    return ReplyKeyboardMarkup(keyboard=[['🔶 Yeni Kanal Ekle', KeyboardButton("🗑️ Kanal Sil", web_app=WebAppInfo(f"https://pharex.dev/otoposterbot/sil-menu?user={user}"))], [KeyboardButton("▶️ SFS Modu", web_app=WebAppInfo(f"https://pharex.dev/otoposterbot/sfs-menu?user={user}")), KeyboardButton('💠 Tür Değiştir', web_app=WebAppInfo(f"https://pharex.dev/otoposterbot/icerik-menu?user={user}"))], ['↩️ Ana Menü']], resize_keyboard=True, selective=True)

def postmenumark(degi):
    if degi:
        return ReplyKeyboardMarkup(keyboard=[['⛓️ Elle Post Paylaş', '⏱ Zamanladıklarım'], ['🔧 Kaynak', '♋️ Özel Kaynak Ayarları'], ['📏 Şablon'], ['↩️ Ana Menü']], resize_keyboard=True, selective=True)
    else:
        return ReplyKeyboardMarkup(keyboard=[['⛓️ Elle Post Paylaş', '⏱ Zamanladıklarım'], ['🔧 Kaynak', '♋️ Özel Kaynak Oluştur'], ['📏 Şablon'], ['↩️ Ana Menü']], resize_keyboard=True, selective=True)

def apimenumark():
    return ReplyKeyboardMarkup(keyboard=[['♻️ API değiştir', '🔗 Site değiştir'], ['🤖 Alternatif Link'], ['↩️ Ana Menü']], resize_keyboard=True, selective=True)

def ekstralarmenumark(user):
    return ReplyKeyboardMarkup(keyboard=[['🍎 iOS Ban Kontrol'], [KeyboardButton("📌 Post Sabitleme", web_app=WebAppInfo(f"https://pharex.dev/otoposterbot/pin-menu?user={user}"))], ['🔁 Tekrarlı Post Paylaş'], ['↩️ Ana Menü']], resize_keyboard=True, selective=True)

def imark():
    imark = ReplyKeyboardMarkup(keyboard=[['❌ İptal']], one_time_keyboard=True, resize_keyboard=True, selective=True)
    return imark

def webappmark(user, chose):
    wappmark = []
    webappsatir = []
    user_data = collection.find_one({"_id": user})
    if chose == -1:
        kanal_listesi = user_data['kanal']
    else:
        kanal_listesi = [user_data['kanal'][chose]]
    for wpam in kanal_listesi:
        try:
            kanal_ismi = bot.get_chat(int(wpam)).title
        except:
            continue
        kaynaklistesi = []
        for kaynak in KaynakCol.find({}):
            if kaynak['no'] in ignorekaynak:
                continue
            kobj = {'kaynak': False, "isim": "Kaynağa Ulaşılamadı!", "link": "t.me/otoposterbotlog", "zaman": "Henüz ayarlanmamış", "no": "0"}
            if kaynak['icerik'] == "+18" and wpam not in user_data['icerik'] or kaynak['icerik'] == "arsiv" and wpam in user_data['icerik']:
                if user in kaynak['kaynak'] and wpam in kaynak['kanal']:
                    kobj['kaynak'] = True
            else:        
                continue
            kobj['isim'] = kaynak.get('title', "yok")
            kobj['link'] = kaynak.get('link', "yok")
            kobj['zaman'] = kaynak['zaman']
            kobj['no'] = kaynak['no']
            kaynaklistesi.append(kobj)
        wappmark.append(KeyboardButton(text=kanal_ismi, web_app=WebAppInfo(f"https://pharex.dev/otoposterbot/kaynak-menu?kanal={wpam[1:]}&user={user}")))
        if len(wappmark) == 2:
            webappsatir.append(wappmark)
            wappmark = []
        cevap = "Hata"
        cevap = ReqPost("https://pharex.dev/otoposterbot/kaynak-menu", json={"data": kaynaklistesi, "user_id": user, "kanal_id": wpam, "kanal_ismi": kanal_ismi}, headers=headerss).text

    try:
        bot.send_message(sahip, cevap) if cevap != "Veri aktarıldı!" else None
        print(str(cevap))
    except:
        pass
    
    webappsatir.append(wappmark)
    webappsatir.append([KeyboardButton("↩️ Ana Menü")])
    if chose == -1:
        return ReplyKeyboardMarkup(webappsatir, resize_keyboard=True)
    else:
        return ReplyKeyboardMarkup([[]])


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

def tekrarlipostkan(user, context):
    tpk = []
    for tkan in collection.find_one({"_id": user})['kanal']:
        try:
            tkanisim = bot.get_chat(tkan).title
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

def sfsmark(user):
    sfs_dat = collection.find_one({"_id": user})
    sfsbutno = 0
    sfskeyb = []
    for sfskan in sfs_dat['kanal']:
        sfsobje = {}
        try:
            sfschatg = bot.get_chat(sfskan)
        except:
            continue
        sfsobje['sfs'] = True if sfskan in sfs_dat['eski'] else False
        sfsobje['link'] = sfschatg.invite_link
        sfsobje['isim'] = sfschatg.title
        sfsobje['no'] = sfskan
        sfskeyb.append(sfsobje)

    ReqPost("https://pharex.dev/otoposterbot/sfs-menu", json={"data": sfskeyb, "user_id": user}, headers=headerss).text

    return KeyboardButton("▶️ SFS Modu", web_app=WebAppInfo(f"https://pharex.dev/otoposterbot/sfs-menu?user={user}"))

def pinmark(user):
    pin_dat = collection.find_one({"_id": user})
    pinkeyb = []
    for pinkan in pin_dat['kanal']:
        pinobje = {}
        try:
            pinchatg = bot.get_chat(pinkan)
        except:
            continue
        pinobje['pin'] = True if pinkan in pin_dat['pin'] else False
        pinobje['link'] = pinchatg.invite_link
        pinobje['isim'] = pinchatg.title
        pinobje['no'] = pinkan
        pinkeyb.append(pinobje)

    ReqPost("https://pharex.dev/otoposterbot/pin-menu", json={"data": pinkeyb, "user_id": user}, headers=headerss).text

    return KeyboardButton("📌 Post Sabitleme", web_app=WebAppInfo(f"https://pharex.dev/otoposterbot/pin-menu?user={user}"))

def dagme():
    dagme = ReplyKeyboardMarkup(keyboard=[['📝 Kaydet']], row_width=2, one_time_keyboard=True, resize_keyboard=False, selective=True)
    return dagme

def altsitemarkup(asite):
    asmark = InlineKeyboardMarkup([[InlineKeyboardButton("TRLink", callback_data=f"{asite}-1")], [InlineKeyboardButton("PND.TL", callback_data=f"{asite}-2")], [InlineKeyboardButton("Exe.io", callback_data=f"{asite}-3")], [InlineKeyboardButton("Ouo.io", callback_data=f"{asite}-4")], [InlineKeyboardButton("Pubiza", callback_data=f"{asite}-5")], [InlineKeyboardButton("Gir.ist", callback_data=f"{asite}-6")], [InlineKeyboardButton("Cuty.io", callback_data=f"{asite}-8")], [InlineKeyboardButton("ShrtFly", callback_data=f"{asite}-9")], [InlineKeyboardButton("Urlcik.XYZ", callback_data=f"{asite}-7")], [InlineKeyboardButton("Za.gl", callback_data=f"{asite}-10")], [InlineKeyboardButton("Link Perisi", callback_data=f"{asite}-11")], [InlineKeyboardButton("kiw.app", callback_data=f"{asite}-11")], [InlineKeyboardButton("❌ İptal ❌", callback_data="iptal")]])
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

def icerikmark(user):
    icerik_dat = collection.find_one({"_id": user})
    icerikbutno = 0
    icerikkeyb = []
    for icerikkan in icerik_dat['kanal']:
        icerikobje = {}
        try:
            icerikchatg = bot.get_chat(icerikkan)
        except:
            continue
        icerikobje['icerik'] = True if icerikkan in icerik_dat['icerik'] else False
        icerikobje['link'] = icerikchatg.invite_link
        icerikobje['isim'] = icerikchatg.title
        icerikobje['no'] = icerikkan
        icerikkeyb.append(icerikobje)

    ReqPost("https://pharex.dev/otoposterbot/icerik-menu", json={"data": icerikkeyb, "user_id": user}, headers=headerss).text

    return KeyboardButton('💠 Tür Değiştir', web_app=WebAppInfo(f"https://pharex.dev/otoposterbot/icerik-menu?user={user}"))

def okaykanalmark(user):
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
            okaykname = bot.get_chat(okaykkan).title
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
            kmark = InlineKeyboardMarkup([[InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk")], [InlineKeyboardButton("🤖 Botlog Oluştur 🤖", callback_data="logokay")], [InlineKeyboardButton("🌐 Bağlı Kanallarım 🌐", callback_data="okaykanal")], [InlineKeyboardButton("💣 Kaynağı Yok Et 💣", callback_data="eminmisin")], [InlineKeyboardButton("Kaynak Tür: "+ozicerik['isim'], callback_data=ozicerik['data'])], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
        else:
            kmark = InlineKeyboardMarkup([[InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk")], [InlineKeyboardButton("🤖 Botlog Kaldır ❌", callback_data="logokaldir")], [InlineKeyboardButton("🌐 Bağlı Kanallarım 🌐", callback_data="okaykanal")], [InlineKeyboardButton("💣 Kaynağı Yok Et 💣", callback_data="eminmisin")], [InlineKeyboardButton("Kaynak Tür: "+ozicerik['isim'], callback_data=ozicerik['data'])], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
    else:
        kmark = InlineKeyboardMarkup([[InlineKeyboardButton("🟣 Özel Kaynağı Kaldır 🟣", callback_data="okayk")], [InlineKeyboardButton("🌐 Bağlı Kanallarım 🌐", callback_data="okaykanal")], [InlineKeyboardButton("❌ İptal ❌", callback_data="aiptal")]])
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

def patmark(user):
    zero = 0
    pkeyb = [[InlineKeyboardButton("💎Hepsine Gönder💎", callback_data="pat-0")]]
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
