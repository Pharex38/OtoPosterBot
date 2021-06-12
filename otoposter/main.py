from telegram.ext import Updater, Defaults 
from importlib import import_module
from .modules import ALL_MODULES
from telegram import ParseMode
from . import *


for module_name in ALL_MODULES:
    imported_module = import_module("otoposter.modules." + module_name)


updater = Updater(token=bottoken, defaults=Defaults(parse_mode=ParseMode.HTML, run_async=True, timeout=90), request_kwargs={'con_pool_size': 999, 'read_timeout': 150, 'connect_timeout': 150})

updater.start_polling()
updater.idle()

