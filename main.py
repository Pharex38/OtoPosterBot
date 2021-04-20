from YaDiskClient.YaDiskClient import YaDisk
import telethon
from os impoet environ

disk = YaDisk(alperekocakaplan31, 5454562121a)

@bot.message_handler(commands=['start'])
def start(m):
    chat = m.chat.id
    gui = disk.df()
    bot.send_message(chat, gui)