# OtoPosterBot

## ❔Ne İşe Yarıyor? 
Bu bot sizin seçtiğiniz kaynak kanalında paylaşılan postların linklerini otomatik olarak kısaltıp sizin kanalınızda paylaşır.

## ❔Nasıl Kullanılır?
1. Adım: Botu kanlınıza yönetici olarak ekleyin.
2. Adım: Kaydet butonunu kullanarak bilgilerinizi kaydedin.
3. Adım: KANALINIZDA /onayla yazın.
4. Adım: Keyfini çıkarın.

## ❔Senin Kazancın Nedir?
Kanalınıza atılan yirmi linkten birisi benim API adresim ile kısaltılır.

---

## Teknik Özet

Telegram kanal otomasyonu: seçilen kaynak kanalı dinler, paylaşılan gönderileri hedef
kanala aktarır, içindeki bağlantıları kısaltır ve zamanlanmış gönderimleri yönetir.

**Yığın:** Python 3.9 · `python-telegram-bot` (bot arayüzü) · `Pyrogram` + `TgCrypto`
(kullanıcı oturumu üzerinden kanal okuma) · `MongoDB` / `pymongo` (kanal, kaynak, buton
ve istek koleksiyonları) · `APScheduler` (zamanlanmış gönderim) · `matplotlib` (istatistik
grafikleri)

**Yapı:**

| Dosya | İş |
| --- | --- |
| `main.py` | bot süreci, handler kaydı |
| `TimerEklenti.py` | ayrı worker — zamanlanmış gönderimler |
| `OtoPoster/poster.py` | gönderi aktarma ve link dönüştürme |
| `OtoPoster/callbacks.py` | buton akışları (en büyük modül, ~800 satır) |
| `OtoPoster/jobs.py` | periyodik işler |
| `OtoPoster/komutlar.py` · `markups.py` | komutlar ve klavye tanımları |
| `OtoPosterPersistence/` | bot durumunun kalıcılaştırılması |

İki worker olarak koşar (`Procfile`): bot ve zamanlayıcı ayrı süreçlerde.

**Ölçek:** ~4.900 satır Python, 4.500+ commit, Mart 2021 – Eylül 2026.

**Yapılandırma:** bağlantı bilgileri ortam değişkenlerinden okunur, örnekler
`.env.example` dosyasında. Depoda kimlik bilgisi tutulmaz.

---

### ❤️ Geliştirici: [@Pharex](https://t.me/Pharex)

 
### 📔        [@OtoPosterBotLog](https://t.me/OtoPosterBotLog)
