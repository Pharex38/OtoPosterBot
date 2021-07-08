from telethon import *
import logging, os, datetime, time, asyncio, pytz
from ssl import CERT_NONE
from pymongo import *
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.messages import GetScheduledHistoryRequest
from telethon.errors.rpcbaseerrors import *

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
app_str = maindata['string']

app = TelegramClient("app_str", api_id, api_hash).start()



@app.on(events.NewMessage(incoming=True, from_users=opb))
async def islem(event):
	if event.raw_text.startswith("-"):
		async with event.client.conversation(event.chat_id) as conv:
			raws = event.raw_text.split("+")
			try:
				kan = await event.client.get_entity(int(raws[0]))
			except FloodError as ex:
				time.sleep(ex.x)
			except:
				collection.update_one({"_id": user}, {"$set": {"vakit": 0}})
				await app.send_message(opb, str(user)+"+"+str("Eklentiyi kanaldan çıkardığınız Post Zamanalama özelliği devre dışı bırakıldı."))
				return
			user = int(raws[2])
			dlc = int(raws[1])
			trysch = 0
			user_dat = collection.find_one({"_id": int(user)})
			while True:
				if dlc >= len(user_dat['vakit']):
					dlc = 0
				raw_vakit = user_dat['vakit'][dlc]
				bugün = datetime.datetime.now()
				raw_vakit = str(bugün.day).zfill(2) + "/" + str(bugün.month).zfill(2) + "/" + str(bugün.year) + " " + str(raw_vakit) + ":59"
				tvakit = datetime.timedelta(hours = 3)
				vakit = datetime.datetime.strptime(raw_vakit, '%d/%m/%Y %H:%M:%S') - tvakit
				kontrol = vakit - datetime.datetime.utcnow()
				if not kontrol.days < 0:
					break
				if trysch > len(user_dat['vakit']):
					return
				dlc += 1
				trysch += 1
			post = await conv.wait_event(events.NewMessage(incoming=True, from_users=opb))
			print(dlc)
			try:
				await app.send_file(entity=kan, file=post.message.media, caption=post.message.raw_text, schedule=vakit)
			except:
				collection.update_one({"_id": user}, {"$set": {"vakit": 0}})
				await app.send_message(opb, str(user)+"+"+str("Eklentiyi kanaldan çıkardığınız Post Zamanalama özelliği devre dışı bırakıldı."))
			else:
				collection.update_one({"_id": user}, {"$set": {"time": dlc+1}})
			histor = await app(GetScheduledHistoryRequest(kan, hash=0))
			#print(histor)
	else:
		try:
			await app(ImportChatInviteRequest(event.raw_text.split("/")[-1]))
		except:
			pass



logger.info("Bot Başlatıldı!")
app.run_until_disconnected()


