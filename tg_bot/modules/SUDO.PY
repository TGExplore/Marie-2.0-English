import html

from typing import List

from telegram import Update, Bot
from telegram.ext import CommandHandler, Filters
from telegram.ext.dispatcher import run_async

from tg_bot import dispatcher, SUDO_USERS, OWNER_USERNAME, OWNER_ID
from tg_bot.modules.helper_funcs.extraction import extract_user
from tg_bot.modules.helper_funcs.chat_status import bot_admin


@bot_admin
@run_async
def addsudo(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    banner = update.effective_user
    user_id = extract_user(message, args)
    
    if not user_id:
        message.reply_text("Refer a user first....")
        return ""
        
    if int(user_id) == OWNER_ID:
        message.reply_text("The specified user is my owner! No need add him to SUDO_USERS list!")
        return ""
        
    if int(user_id) in SUDO_USERS:
        message.reply_text("Buddy this user is already a sudo user.")
        return ""
    
    with open("sudo_users.txt","a") as file:
        file.write(str(user_id) + "\n")
    
    SUDO_USERS.append(user_id)
    message.reply_text("Succefully Added To SUDO List!")
        
    return ""

@bot_admin
@run_async
def rsudo(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    user_id = extract_user(message, args)
    
    if not user_id:
        message.reply_text("Refer the user first.")
        return ""

    if int(user_id) == OWNER_ID:
        message.reply_text("The specified user is my owner! I won't remove him from SUDO_USERS list!")
        return ""
    
    if user_id not in SUDO_USERS:
        message.reply_text("{} is not a sudo user".format(user_id))
        return ""

    users = [line.rstrip('\n') for line in open("sudo_users.txt")]

    with open("sudo_users.txt","w") as file:
        for user in users:
            if not int(user) == user_id:
                file.write(str(user) + "\n")

    SUDO_USERS.remove(user_id)
    message.reply_text("Yep Succefully removed from SUDO List!")
    
    return ""


__help__ = """
*Bot owner only:*
 - /addsudo: promotes the user to SUDO USER
 - /rsudo: demotes the user from SUDO USER
"""

__mod_name__ = "Sudo"

addsudo_HANDLER = CommandHandler("addsudo", addsudo, pass_args=True, filters=Filters.user(OWNER_ID))
rsudo_HANDLER = CommandHandler("rsudo", rsudo, pass_args=True, filters=Filters.user(OWNER_ID))

dispatcher.add_handler(addsudo_HANDLER)
dispatcher.add_handler(rsudo_HANDLER)
