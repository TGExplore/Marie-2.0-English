from typing import Optional, List

from telegram import Message, Update, Bot, User
from telegram import MessageEntity, ParseMode
from telegram.ext import Filters, MessageHandler, run_async

from tg_bot import dispatcher, LOGGER
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.extraction import extract_text
from py_translator import translator
from googletrans import Translator

@run_async
def do_translate(bot: Bot, update: Update, args: List[str]):
    short_name = "Created By @MidukkiBot 😬"
    msg = update.effective_message # type: Optional[Message]
    lan = " ".join(args)
    to_translate_text = msg.reply_to_message.text
    translator = Translator()
    try:
        translated = translator.translate(to_translate_text, dest=lan)
        src_lang = translated.src
        translated_text = translated.text
        msg.reply_text("Translated from {} to {}.\n {}".format(src_lang, lan, translated_text))
    except exc:
        msg.reply_text(str(exc))


__help__ = """- /tr - as reply to a long message
You can translate words or phrases using this command as reply to a long message. 
"""
__mod_name__ = "Translator"

dispatcher.add_handler(DisableAbleCommandHandler("tr", translate, pass_args=True))
