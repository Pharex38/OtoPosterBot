from . import *
from .jobs import *
from .markups import *
from .misc import *



def poster(update, context):
    global postsirasi
    pochat = update.channel_post.chat.id
    # Ana Kaynaklar
    if KaynakCol.find_one({"_id": pochat}) != None:
        logger.warning(f"{update.channel_post.chat.title} Postu sıraya eklendi.")
        postdict = {"chatid": pochat, "update": update}
        postsirasi.append(postdict)
    # Özel Kaynaklar
    elif OzelCol.find_one({"okaynak": pochat}) != None:
        logger.warning(f"[ÖZEL] {update.channel_post.chat.title} Postu sıraya eklendi.")
        opostdict = {"chatid": pochat, "update": update}
        opostsirasi.append(opostdict)

