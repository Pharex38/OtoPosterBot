from telegram.ext import Updater, Defaults, CallbackContext 
from importlib import import_module
from .modules import ALL_MODULES
from telegram import ParseMode
import traceback
from . import *
import html
import json

for module_name in ALL_MODULES:
    imported_module = import_module("otoposter.modules." + module_name)


def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(msg="Bir Hata oluştu:", exc_info=context.error)
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'BİR HATA OLUŞTU!\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )
    for i in adminlist:
        context.bot.send_message(chat_id=i, text=message, parse_mode=ParseMode.HTML)


def main() -> None:
    updater = Updater(token=bottoken, defaults=Defaults(parse_mode=ParseMode.HTML, run_async=True, timeout=90), request_kwargs={'con_pool_size': 999, 'read_timeout': 150, 'connect_timeout': 150})

    dispatcher = updater.dispatcher

    updater.job_queue

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


main()
