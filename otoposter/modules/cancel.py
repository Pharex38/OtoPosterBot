from otoposter import *
from .misc import dugme

def cancel(update, context):
    chat = update.message.chat.id
    bot.send_message(chat, "İptal Edildi.", reply_markup=dugme(chat))
    return
