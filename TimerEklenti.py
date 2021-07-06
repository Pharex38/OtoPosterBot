from telethon import *
import logging, os, datetime, time, asyncio, pytz
from ssl import CERT_NONE
from pymongo import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

opb = 1742595887
sahip = 1302980840
opb = sahip

mpass = os.environ['MONGOPASS']
mongo = f"os.environ["MONGO_URI"]"
cluster = MongoClient(mongo, ssl_cert_reqs=CERT_NONE)

db = cluster["OtoPost"]
collection = db["Kanallar"]

maindata = collection.find_one({"_id": 0})
api_id = maindata['aid']
api_hash = maindata['hash']
app_str = maindata['string']

app = TelegramClient(app_str, api_id, api_hash).start()

@app.on(events.NewMessage(incoming=True, from_users=opb))
async def islem(event):
	if not event.raw_text.startswith("-"):
		return

	async with event.client.conversation(event.chat_id) as conv:
		raws = event.raw_text.split("+")
		kan = await event.client.get_entity(int(raws[0]))
		user = raws[2]
		dlc = int(raws[1])
		user_dat = collection.find_one({"_id": int(user)})
		while True:
			raw_vakit = user_dat['vakit'][dlc]

			bugün = datetime.datetime.now()
			raw_vakit = str(bugün.day).zfill(2) + "/" + str(bugün.month).zfill(2) + "/" + str(bugün.year) + " " + str(raw_vakit) + ":00"
			
			print(datetime.datetime.utcnow())
			tvakit = datetime.timedelta(hours = 3)
			
			vakit = datetime.datetime.strptime(raw_vakit, '%d/%m/%Y %H:%M:%S') - tvakit
			print(vakit)
			
			kontrol = vakit - datetime.datetime.utcnow()
			if not kontrol.days < 0:
				break
			dlc += 1
		
		post = await conv.wait_event(events.NewMessage(incoming=True, from_users=opb))

		await app.send_file(entity=kan, file=post.message.media, caption=post.message.raw_text, schedule=vakit)




logger.info("Bot Başlatıldı!")
app.run_until_disconnected()


