from gpytranslate import Translator
from pyrogram import filters
from pyrogram.types import Message

from tg_bot import pg


trans = Translator()


@pg.on_message(filters.command(["tl", "tr"]))
async def translate(_, message: Message) -> None:
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("Reply to a message to translate it!")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "en"
    translation = await trans(to_translate,
                              sourcelang=source, targetlang=dest)
    reply = f"<b>Translated from {source} to {dest}</b>:\n" \
        f"<code>{translation.text}</code>"

    await message.reply_text(reply, parse_mode="html")


@pg.on_message(filters.command("langs"))
async def languages(_, message: Message) -> None:
    await message.reply_text(
        "Click [here](https://cloud.google.com/translate/docs/languages)"
        " to see the list of supported language codes!",
        disable_web_page_preview=True
    )


__mod_name__ = "Translation"

__help__ = """
Use this module to translate stuff... duh!
*Commands:*
• `/tl` (or `/tr`): as a reply to a message, translates it to English.
• `/tl <lang>`: translates to <lang>
eg: `/tl ja`: translates to Japanese.
• `/tl <source>//<dest>`: translates from <source> to <lang>.
eg: `/tl ja//en`: translates from Japanese to English.
• `/langs`: get a list of supported languages for translation."""
