from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton
from otoposter import bot

kaynaklar = [-1001368112299, -1001122395785, -1001423365614, -1001240514861, -1001405966343, -1001368008488, -1001379893661]

for i in kaynaklar:
    index = int(kaynaklar.index(i))
    if index == 0:
        try:
            mahzen = bot.get_chat(kaynaklar[0]) 
        except:
            bildir('Link Mahzeni kaynağına bot ulaşamıyor')
    elif index == 1:
        try:
            bedava = bot.get_chat(kaynaklar[1])
        except:
            bildir('Bedava Linkler kaynağına bot ulaşamıyor')
    elif index == 2:
        try:
            evi = bot.get_chat(kaynaklar[2])
        except:
            bildir('Link Evi kaynağına bot ulaşamıyor')
    elif index == 3:
        try:
           bashub = bot.get_chat(kaynaklar[3])
        except:
           bildir('Başhub kaynağına bot ulaşamıyor')
    elif index == 4:
        try:
            acikmi = bot.get_chat(kaynaklar[4])
        except:
            bildir('Açık mı kaynağına bot ulaşamıyor')
    elif index == 5:
        try:
            muho = bot.get_chat(kaynaklar[5])
        except:
            bildir('Muho kaynağına bot ulaşamıyor')
    elif index == 6:
        try:
            tutan = bot.get_chat(kaynaklar[6])
        except:
            bildir('Tutan kaynağına bot ulaşamıyor')
    else:
        qqq = 'Bu ne ? : {}'.format(i)
        bildir(qqq)


kara = karaliste['kara']

ALTMENU, APIDEGISTIR, KANALKAYDET = range(3)

OZELKAYNAK = range(1)

OZELBOTLOG = range(1)

ALTAPI = range(1)

SABLON = range(1)

PATPOST = range(1)

markup = ForceReply(selective=False)

def dugme(user):
    first = collection.find_one({'_id': user})
    if first == None:
        return ReplyKeyboardMarkup(keyboard=[['📝 Kaydet']], row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)

    dugme = ReplyKeyboardMarkup(keyboard=[['⚙️ Menü'], ['🔧 Kaynak', '📏 Şablon'], ['▶️ SFS Modu', '🥰 Bağış'], ['⛓️ Elle Post Paylaş']], resize_keyboard=True)
    
    return dugme

def markupp():
    markupp = ReplyKeyboardMarkup(keyboard=[['🔶 Yeni Kanal Ekle', '🗑️ Kanal Sil'], ['♻️ API değiştir', '🔗 Site değiştir'], ['🤖 Alternatif Ekle'], ['↩️ Ana Menü']], row_width=2, one_time_keyboard=True, resize_keyboard=True)

    return markupp

def imark():
    imark = ReplyKeyboardMarkup(keyboard=[['❌ İptal']], one_time_keyboard=True, resize_keyboard=True, selective=True)

    return imark

def dagme():
    dagme = ReplyKeyboardMarkup(keyboard=[['📝 Kaydet']], row_width=2, one_time_keyboard=True, resize_keyboard=True, selective=True)

    return dagme
