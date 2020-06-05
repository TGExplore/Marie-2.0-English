import sys
import traceback

from functools import wraps
from typing import Optional

from telegram import User, Chat, ChatMember, Update, Bot
from telegram import error

from tg_bot import dispatcher, DEL_CMDS, SUDO_USERS, WHITELIST_USERS, LOGGER, MESSAGE_DUMP

from tg_bot.modules import translations

def send_message(message, text, target_id=None, *args,**kwargs):
	if not target_id:
		try:
			return message.reply_text(text, *args,**kwargs)
		except error.BadRequest as err:
			if str(err) == "Reply message not found":
				try:
					return message.reply_text(text, quote=False, *args, **kwargs)
				except error.BadRequest as err:
					LOGGER.exception("ERROR: {}".format(err))
			elif str(err) == "Have no rights to send a message":
				try:
					dispatcher.bot.leaveChat(message.chat.id)
					dispatcher.bot.sendMessage(MESSAGE_DUMP, "I left `{}`\nBecause of: `Muted`".format(message.chat.title))
				except error.BadRequest as err:
					if str(err) == "Chat not found":
						pass
			else:
				LOGGER.exception("ERROR: {}".format(err))
	else:
		try:
			dispatcher.bot.send_message(target_id, text, *args, **kwarg)
		except error.BadRequest as err:
			LOGGER.exception("ERROR: {}".format(err))

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_chat.id, action=action)
            return func(update, context,  *args, **kwargs)
        return command_func

    return decorator
