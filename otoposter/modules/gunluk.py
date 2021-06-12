from otoposter import *
import threading

def gunluk():
    while 0 < 1:
        zaman = datetime.datetime.now()
        if zaman.hour == 11 and zaman.minute == 50:
            msg = bot.send_message(botlog, "<code>Günlük veriler hesaplanıyor...</code>")
            toplam = 0
            kum = []
            kanals = 0
            users = 0
            kullanicilar = collection.find({})
            for kullanici in kullanicilar:
                users += 1
                for kul in kullanici['kanal']:
                    if not kul in kum:
                        kum.append(kul)
                        time.sleep(0.5)
                        try:
                            uye = bot.get_chat_members_count(kul)
                            print(uye)
                        except Exception as e:
                            logger.error(e)
                            time.sleep(30)
                        else:
                            toplam += uye
                            kanals += 1
          
            toplam = toplam / 1000
            toplam = str(round(toplam, 1))+"K" if round(toplam, 1) < 1000 else str(round(toplam / 1000, 1))+"M"
            msg = bot.edit_message_text("👥 Toplam Kullanıcı Sayısı: {}\n📢 Toplam Kayıtlı Kanal Sayısı: {}\n🙋 Toplam Kitle: {}\n\nHer gün saat 22:00'da otomatik olarak güncel veriler paylaşılacak.".format(users, kanals, toplam), botlog, msg.message_id)
            bot.pin_chat_message(botlog, msg.message_id)
        time.sleep(60)
    
threading.Thread(target=gunluk).start()
