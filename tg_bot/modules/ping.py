from telegram import Update, Bot
from telegram.ext import run_async

from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot import dispatcher

from requests import get


@run_async
def ping(bot: Bot, update: Update):
    start_time = time.time()
    requests.get('https://api.telegram.org')
    end_time = time.time()
    ping_time = round((end_time - start_time), 3)
    update.effective_message.reply_text("PONG!!\n`{}s`".format(ping_time), parse_mode=ParseMode.MARKDOWN)


__mod_name__ = "Ping"

PING_HANDLER = DisableAbleCommandHandler("ping", ping)

dispatcher.add_handler(PING_HANDLER)
