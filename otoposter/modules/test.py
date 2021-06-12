from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    Defaults,
    ExtBot,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)
from otoposter.main import *

def test(update, context):
    user = update.message.from_user.id
    chat = update.message.chat.id
    bot = context.bot
    bot.send_message(chat, "🥰 I'm Alive!")


dispatcher.add_handler(CommandHandler('test', start, Filters.update.message & Filters.chat_type.private))
