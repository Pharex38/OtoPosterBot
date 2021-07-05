from telethon import *
import logging, os, datetime, time, asyncio
from ssl import CERT_NONE
from pymongo import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

opb = 1742595887
sahip = 1302980840

mpass = os.environ['MONGOPASS']
mongo = f"os.environ["MONGO_URI"]"
cluster = MongoClient(mongo, ssl_cert_reqs=CERT_NONE)

db = cluster["OtoPost"]
collection = db["Kanallar"]

maindata = collection.find_one({"_id": 0})
api_id = maindata['aid']
api_hash = maindata['hash']

app = TelegramClient("Timer", api_id, api_hash).start()

@app.on(events.NewMessage(incoming=True, from_users=sahip))
async def islem(event):
	if not event.raw_text.startswith("-"):
		return
	kan = await event.client.get_entity(int(event.raw_text))
	async with event.client.conversation(event.chat_id) as conv:
		raw_vakit = await conv.wait_event(events.NewMessage(incoming=True, from_users=sahip))
		bugün = datetime.datetime.now()
		raw_vakit = str(bugün.year) + "/" + str(bugün.month) + "/" + str(bugün.day) + " " + str(raw_vakit) + ":00"
		vakit = datetime.datetime.strptime(raw_vakit, '%d/%m/%y %H:%M:%S')
		post = await conv.wait_event(events.NewMessage(incoming=True, from_users=sahip))
		if post.message:
			pass
		await app.send_file(entity=kan, file=post.message.media, caption=post.message.raw_text, schedule=)




logger.info("Bot Başlatıldı!")
app.run_until_disconnected()


xor = Message(id=4371, peer_id=PeerChannel(channel_id=1391561285), date=datetime.datetime(2021, 7, 5, 9, 51, 23, tzinfo=datetime.timezone.utc), message='🌟Vur Aşkım Vur Sikicim Benim\n\nAntalyanın En Sağlam Escortunu Otelde Bağırtarak Sikiyor🔞🔥\n\n🔗 https://streamtape.com/v/ZbLvgdDWJkIqWBL/9.mp4\n\n⭕️Link nasıl geçilir: @kamlinkgecis', out=False, mentioned=False, media_unread=False, silent=False, post=False, from_scheduled=False, legacy=False, edit_hide=False, pinned=False, from_id=PeerUser(user_id=1302980840), fwd_from=MessageFwdHeader(date=datetime.datetime(2021, 7, 2, 20, 20, 49, tzinfo=datetime.timezone.utc), imported=False, from_id=PeerChannel(channel_id=1450479011), from_name=None, channel_post=77, post_author=None, saved_from_peer=None, saved_from_msg_id=None, psa_type=None), via_bot_id=None, reply_to=None, media=MessageMediaDocument(document=Document(id=5877431147054500803, access_hash=28633969434880850, file_reference=b"\x02R\xf1\x8aE\x00\x00\x11\x13`\xe2\xd6\x1b\x1f\xfe\x02\x19](['\xe5\x9e\xcf\x92\x97wr^", date=datetime.datetime(2021, 5, 29, 15, 6, 57, tzinfo=datetime.timezone.utc), mime_type='video/mp4', size=1424429, dc_id=4, attributes=[DocumentAttributeVideo(duration=10, w=406, h=720, round_message=False, supports_streaming=True), DocumentAttributeFilename(file_name='000.mp4')], thumbs=[PhotoStrippedSize(type='i', bytes=b'\x01(\x16\x83P\x93\xa0\xc7n\xb5\x9e+^\xee\x0f1\x00\xfdj\xa4V\x12o\x19 \nWH\xab6Z\xd3T=\xb9\xdc:\x1cQV\xe1A\x1cx\x14SBc3\xbd~\x82\x90\x1c\x11M\x8c\x80\x01\x07\x82(\x90\xe0q\xc1\xa9\x96\xa5\xad\t\xf26\xf5\x14Vd\xb22\xb9\xdd\x90O\xa5\x14"X\xe6\x93\xcar\xa7\xa0\xefQ\xcbq\x95\x04r3E\x14Xw\x1c\xc6\x16PenOAE\x14Q`\xb9'), PhotoSize(type='m', location=FileLocationToBeDeprecated(volume_id=400245900342, local_id=6498), w=180, h=320, size=7411)], video_thumbs=[]), ttl_seconds=None), reply_markup=None, entities=[MessageEntityUrl(offset=96, length=46), MessageEntityMention(offset=166, length=13)], views=1, forwards=7, replies=MessageReplies(replies=0, replies_pts=6777, comments=False, recent_repliers=[], channel_id=None, max_id=None, read_max_id=None), edit_date=None, post_author=None, grouped_id=None, restriction_reason=[], ttl_period=None)


