from telethon import *
import logging, os, datetime, time, asyncio
from ssl import CERT_NONE
from pymongo import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

opb = 1742595887

mpass = os.environ['MONGOPASS']
mongo = f"os.environ["MONGO_URI"]"
cluster = MongoClient(mongo, ssl_cert_reqs=CERT_NONE)

db = cluster["OtoPost"]
collection = db["Kanallar"]

maindata = collection.find_one({"_id": 0})
api_id = maindata['aid']
api_hash = maindata['hash']

app = TelegramClient("Timer", api_id, api_hash).start()

@app.on(events.NewMessage(incoming=True, from_users=opb))
async def islem(event):
	if not event.raw_text.startswith("-"):
		return
	kan = event.raw_text
	async with event.client.conversation(event.chat_id) as conv:
		await event.client.send_message(event.chat_id, ".")
		vakit = await conv.wait_event(events.NewMessage(incoming=True, from_users=opb))

		await event.client.send_message(event.chat_id, ".")
		post = await conv.wait_event(events.NewMessage(incoming=True, from_users=opb))

		print(post.message)


logger.info("Bot Başlatıldı!")
app.run_until_disconnected()
