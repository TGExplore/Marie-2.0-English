import requests
import DeadlyBot.modules.hentai as hemtai
from PIL import Image
import os

from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async

from DeadlyBot import dispatcher, updater


def is_user_in_chat(chat: Chat, user_id: int) -> bool:
    member = chat.get_member(user_id)
    return member.status not in ("left", "kicked")


@run_async
def neko(update, context):
    msg = update.effective_message
    target = "neko"
    msg.reply_photo(nekos.img(target))


@run_async
def feet(update, context):
    msg = update.effective_message
    target = "feet"
    msg.reply_photo(nekos.img(target))


@run_async
def yuri(update, context):
    msg = update.effective_message
    target = "yuri"
    msg.reply_photo(nekos.img(target))


@run_async
def trap(update, context):
    msg = update.effective_message
    target = "trap"
    msg.reply_photo(nekos.img(target))


@run_async
def futanari(update, context):
    msg = update.effective_message
    target = "futanari"
    msg.reply_photo(nekos.img(target))


@run_async
def hololewd(update, context):
    msg = update.effective_message
    target = "hololewd"
    msg.reply_photo(nekos.img(target))


@run_async
def lewdkemo(update, context):
    msg = update.effective_message
    target = "lewdkemo"
    msg.reply_photo(nekos.img(target))


@run_async
def sologif(update, context):
    msg = update.effective_message
    target = "solog"
    msg.reply_video(nekos.img(target))


@run_async
def feetgif(update, context):
    msg = update.effective_message
    target = "feetg"
    msg.reply_video(nekos.img(target))


@run_async
def cumgif(update, context):
    msg = update.effective_message
    target = "cum"
    msg.reply_video(nekos.img(target))


@run_async
def erokemo(update, context):
    msg = update.effective_message
    target = "erokemo"
    msg.reply_photo(nekos.img(target))


@run_async
def lesbian(update, context):
    msg = update.effective_message
    target = "les"
    msg.reply_video(nekos.img(target))


@run_async
def wallpaper(update, context):
    msg = update.effective_message
    target = "wallpaper"
    msg.reply_photo(nekos.img(target))


@run_async
def lewdk(update, context):
    msg = update.effective_message
    target = "lewdk"
    msg.reply_photo(nekos.img(target))


@run_async
def ngif(update, context):
    msg = update.effective_message
    target = "ngif"
    msg.reply_video(nekos.img(target))


@run_async
def tickle(update, context):
    msg = update.effective_message
    target = "tickle"
    msg.reply_video(nekos.img(target))


@run_async
def lewd(update, context):
    msg = update.effective_message
    target = "lewd"
    msg.reply_photo(nekos.img(target))


@run_async
def feed(update, context):
    msg = update.effective_message
    target = "feed"
    msg.reply_video(nekos.img(target))


@run_async
def eroyuri(update, context):
    msg = update.effective_message
    target = "eroyuri"
    msg.reply_photo(nekos.img(target))


@run_async
def eron(update, context):
    msg = update.effective_message
    target = "eron"
    msg.reply_photo(nekos.img(target))


@run_async
def cum(update, context):
    msg = update.effective_message
    target = "cum_jpg"
    msg.reply_photo(nekos.img(target))


@run_async
def bjgif(update, context):
    msg = update.effective_message
    target = "bj"
    msg.reply_video(nekos.img(target))


@run_async
def bj(update, context):
    msg = update.effective_message
    target = "blowjob"
    msg.reply_photo(nekos.img(target))


@run_async
def nekonsfw(update, context):
    msg = update.effective_message
    target = "nsfw_neko_gif"
    msg.reply_video(nekos.img(target))


@run_async
def solo(update, context):
    msg = update.effective_message
    target = "solo"
    msg.reply_photo(nekos.img(target))


@run_async
def kemonomimi(update, context):
    msg = update.effective_message
    target = "kemonomimi"
    msg.reply_photo(nekos.img(target))


@run_async
def avatarlewd(update, context):
    msg = update.effective_message
    target = "nsfw_avatar"
    with open("temp.png", "wb") as f:
        f.write(requests.get(nekos.img(target)).content)
    img = Image.open("temp.png")
    img.save("temp.webp", "webp")
    msg.reply_document(open("temp.webp", "rb"))
    os.remove("temp.webp")


@run_async
def gasm(update, context):
    msg = update.effective_message
    target = "gasm"
    with open("temp.png", "wb") as f:
        f.write(requests.get(nekos.img(target)).content)
    img = Image.open("temp.png")
    img.save("temp.webp", "webp")
    msg.reply_document(open("temp.webp", "rb"))
    os.remove("temp.webp")


@run_async
def poke(update, context):
    msg = update.effective_message
    target = "poke"
    msg.reply_video(nekos.img(target))


@run_async
def anal(update, context):
    msg = update.effective_message
    target = "anal"
    msg.reply_video(nekos.img(target))


@run_async
def hentai(update, context):
    msg = update.effective_message
    target = "hentai"
    msg.reply_photo(nekos.img(target))


@run_async
def avatar(update, context):
    msg = update.effective_message
    target = "nsfw_avatar"
    with open("temp.png", "wb") as f:
        f.write(requests.get(nekos.img(target)).content)
    img = Image.open("temp.png")
    img.save("temp.webp", "webp")
    msg.reply_document(open("temp.webp", "rb"))
    os.remove("temp.webp")


@run_async
def erofeet(update, context):
    msg = update.effective_message
    target = "erofeet"
    msg.reply_photo(nekos.img(target))


@run_async
def holo(update, context):
    msg = update.effective_message
    target = "holo"
    msg.reply_photo(nekos.img(target))


# def keta(update, context):
#     msg = update.effective_message
#     target = 'keta'
#     if not target:
#         msg.reply_text("No URL was received from the API!")
#         return
#     msg.reply_photo(nekos.img(target))


@run_async
def pussygif(update, context):
    msg = update.effective_message
    target = "pussy"
    msg.reply_video(nekos.img(target))


@run_async
def tits(update, context):
    msg = update.effective_message
    target = "tits"
    msg.reply_photo(nekos.img(target))


@run_async
def holoero(update, context):
    msg = update.effective_message
    target = "holoero"
    msg.reply_photo(nekos.img(target))


@run_async
def pussy(update, context):
    msg = update.effective_message
    target = "pussy_jpg"
    msg.reply_photo(nekos.img(target))


@run_async
def hentaigif(update, context):
    msg = update.effective_message
    target = "random_hentai_gif"
    msg.reply_video(nekos.img(target))


@run_async
def classic(update, context):
    msg = update.effective_message
    target = "classic"
    msg.reply_video(nekos.img(target))


@run_async
def kuni(update, context):
    msg = update.effective_message
    target = "kuni"
    msg.reply_video(nekos.img(target))


@run_async
def waifu(update, context):
    msg = update.effective_message
    target = "waifu"
    with open("temp.png", "wb") as f:
        f.write(requests.get(nekos.img(target)).content)
    img = Image.open("temp.png")
    img.save("temp.webp", "webp")
    msg.reply_document(open("temp.webp", "rb"))
    os.remove("temp.webp")


@run_async
def kiss(update, context):
    msg = update.effective_message
    target = "kiss"
    msg.reply_video(nekos.img(target))


@run_async
def femdom(update, context):
    msg = update.effective_message
    target = "femdom"
    msg.reply_photo(nekos.img(target))


@run_async
def cuddle(update, context):
    msg = update.effective_message
    target = "cuddle"
    msg.reply_video(nekos.img(target))


@run_async
def erok(update, context):
    msg = update.effective_message
    target = "erok"
    msg.reply_photo(nekos.img(target))


@run_async
def foxgirl(update, context):
    msg = update.effective_message
    target = "fox_girl"
    msg.reply_photo(nekos.img(target))


@run_async
def titsgif(update, context):
    msg = update.effective_message
    target = "boobs"
    msg.reply_video(nekos.img(target))


@run_async
def ero(update, context):
    msg = update.effective_message
    target = "ero"
    msg.reply_photo(nekos.img(target))


@run_async
def smug(update, context):
    msg = update.effective_message
    target = "smug"
    msg.reply_video(nekos.img(target))


@run_async
def baka(update, context):
    msg = update.effective_message
    target = "baka"
    msg.reply_video(nekos.img(target))


@run_async
def dva(update, context):
    msg = update.effective_message
    nsfw = requests.get("https://api.computerfreaker.cf/v1/dva").json()
    url = nsfw.get("url")
    # do shit with url if you want to
    if not url:
        msg.reply_text("No URL was received from the API!")
        return
    msg.reply_photo(url)

__mod_name__ = "Lewd"

__help__ = """
 - /neko: Sends Random SFW Neko source Images.
 - /feet: Sends Random Anime Feet Images.
 - /yuri: Sends Random Yuri source Images.
 - /trap: Sends Random Trap source Images.
 - /futanari: Sends Random Futanari source Images.
 - /hololewd: Sends Random Holo Lewds.
 - /lewdkemo: Sends Random Kemo Lewds.
 - /sologif: Sends Random Solo GIFs.
 - /cumgif: Sends Random Cum GIFs.
 - /erokemo: Sends Random Ero-Kemo Images.
 - /lesbian: Sends Random Les Source Images.
 - /wallpaper: Sends Random Wallpapers.
 - /lewdk: Sends Random Kitsune Lewds.
 - /ngif: Sends Random Neko GIFs.
 - /tickle: Sends Random Tickle GIFs.
 - /lewd: Sends Random Lewds.
 - /feed: Sends Random Feeding GIFs.
 - /eroyuri: Sends Random Ero-Yuri source Images.
 - /eron: Sends Random Ero-Neko source Images.
 - /cum: Sends Random Cum Images.
 - /bjgif: Sends Random Blow Job GIFs.
 - /bj: Sends Random Blow Job source Images.
 - /nekonsfw: Sends Random NSFW Neko source Images.
 - /solo: Sends Random NSFW Neko GIFs.
 - /kemonomimi: Sends Random KemonoMimi source Images.
 - /avatarlewd: Sends Random Avater Lewd Stickers.
 - /gasm: Sends Random Orgasm Stickers.
 - /poke: Sends Random Poke GIFs.
 - /anal: Sends Random Anal GIFs.
 - /hentai: Sends Random Hentai source Images.
 - /avatar: Sends Random Avatar Stickers.
 - /erofeet: Sends Random Ero-Feet source Images.
 - /holo: Sends Random Holo source Images.
 - /tits: Sends Random Tits source Images.
 - /pussygif: Sends Random Pussy GIFs.
 - /holoero: Sends Random Ero-Holo source Images.
 - /pussy: Sends Random Pussy source Images.
 - /hentaigif: Sends Random Hentai GIFs.
 - /classic: Sends Random Classic Hentai GIFs.
 - /kuni: Sends Random Pussy Lick GIFs.
 - /waifu: Sends Random Waifu Stickers.
 - /kiss: Sends Random Kissing GIFs.
 - /femdom: Sends Random Femdom source Images.
 - /cuddle: Sends Random Cuddle GIFs.
 - /erok: Sends Random Ero-Kitsune source Images.
 - /foxgirl: Sends Random FoxGirl source Images.
 - /titsgif: Sends Random Tits GIFs.
 - /ero: Sends Random Ero source Images.
 - /smug: Sends Random Smug GIFs.
 - /baka: Sends Random Baka Shout GIFs.
 - /dva: Sends Random D.VA source Images.
"""

LEWDKEMO_HANDLER = CommandHandler("lewdkemo", lewdkemo)
NEKO_HANDLER = CommandHandler("neko", neko)
FEET_HANDLER = CommandHandler("feet", feet)
YURI_HANDLER = CommandHandler("yuri", yuri)
TRAP_HANDLER = CommandHandler("trap", trap)
FUTANARI_HANDLER = CommandHandler("futanari", futanari)
HOLOLEWD_HANDLER = CommandHandler("hololewd", hololewd)
SOLOGIF_HANDLER = CommandHandler("sologif", sologif)
CUMGIF_HANDLER = CommandHandler("cumgif", cumgif)
EROKEMO_HANDLER = CommandHandler("erokemo", erokemo)
LESBIAN_HANDLER = CommandHandler("lesbian", lesbian)
WALLPAPER_HANDLER = CommandHandler("wallpaper", wallpaper)
LEWDK_HANDLER = CommandHandler("lewdk", lewdk)
NGIF_HANDLER = CommandHandler("ngif", ngif)
TICKLE_HANDLER = CommandHandler("tickle", tickle)
LEWD_HANDLER = CommandHandler("lewd", lewd)
FEED_HANDLER = CommandHandler("feed", feed)
EROYURI_HANDLER = CommandHandler("eroyuri", eroyuri)
ERON_HANDLER = CommandHandler("eron", eron)
CUM_HANDLER = CommandHandler("cum", cum)
BJGIF_HANDLER = CommandHandler("bjgif", bjgif)
BJ_HANDLER = CommandHandler("bj", bj)
NEKONSFW_HANDLER = CommandHandler("nekonsfw", nekonsfw)
SOLO_HANDLER = CommandHandler("solo", solo)
KEMONOMIMI_HANDLER = CommandHandler("kemonomimi", kemonomimi)
AVATARLEWD_HANDLER = CommandHandler("avatarlewd", avatarlewd)
GASM_HANDLER = CommandHandler("gasm", gasm)
POKE_HANDLER = CommandHandler("poke", poke)
ANAL_HANDLER = CommandHandler("anal", anal)
HENTAI_HANDLER = CommandHandler("hentai", hentai)
AVATAR_HANDLER = CommandHandler("avatar", avatar)
EROFEET_HANDLER = CommandHandler("erofeet", erofeet)
HOLO_HANDLER = CommandHandler("holo", holo)
TITS_HANDLER = CommandHandler("tits", tits)
PUSSYGIF_HANDLER = CommandHandler("pussygif", pussygif)
HOLOERO_HANDLER = CommandHandler("holoero", holoero)
PUSSY_HANDLER = CommandHandler("pussy", pussy)
HENTAIGIF_HANDLER = CommandHandler("hentaigif", hentaigif)
CLASSIC_HANDLER = CommandHandler("classic", classic)
KUNI_HANDLER = CommandHandler("kuni", kuni)
WAIFU_HANDLER = CommandHandler("waifu", waifu)
LEWD_HANDLER = CommandHandler("lewd", lewd)
KISS_HANDLER = CommandHandler("kiss", kiss)
FEMDOM_HANDLER = CommandHandler("femdom", femdom)
CUDDLE_HANDLER = CommandHandler("cuddle", cuddle)
EROK_HANDLER = CommandHandler("erok", erok)
FOXGIRL_HANDLER = CommandHandler("foxgirl", foxgirl)
TITSGIF_HANDLER = CommandHandler("titsgif", titsgif)
ERO_HANDLER = CommandHandler("ero", ero)
SMUG_HANDLER = CommandHandler("smug", smug)
BAKA_HANDLER = CommandHandler("baka", baka)
DVA_HANDLER = CommandHandler("dva", dva)

dispatcher.add_handler(LEWDKEMO_HANDLER)
dispatcher.add_handler(NEKO_HANDLER)
dispatcher.add_handler(FEET_HANDLER)
dispatcher.add_handler(YURI_HANDLER)
dispatcher.add_handler(TRAP_HANDLER)
dispatcher.add_handler(FUTANARI_HANDLER)
dispatcher.add_handler(HOLOLEWD_HANDLER)
dispatcher.add_handler(SOLOGIF_HANDLER)
dispatcher.add_handler(CUMGIF_HANDLER)
dispatcher.add_handler(EROKEMO_HANDLER)
dispatcher.add_handler(LESBIAN_HANDLER)
dispatcher.add_handler(WALLPAPER_HANDLER)
dispatcher.add_handler(LEWDK_HANDLER)
dispatcher.add_handler(NGIF_HANDLER)
dispatcher.add_handler(TICKLE_HANDLER)
dispatcher.add_handler(LEWD_HANDLER)
dispatcher.add_handler(FEED_HANDLER)
dispatcher.add_handler(EROYURI_HANDLER)
dispatcher.add_handler(ERON_HANDLER)
dispatcher.add_handler(CUM_HANDLER)
dispatcher.add_handler(BJGIF_HANDLER)
dispatcher.add_handler(BJ_HANDLER)
dispatcher.add_handler(NEKONSFW_HANDLER)
dispatcher.add_handler(SOLO_HANDLER)
dispatcher.add_handler(KEMONOMIMI_HANDLER)
dispatcher.add_handler(AVATARLEWD_HANDLER)
dispatcher.add_handler(GASM_HANDLER)
dispatcher.add_handler(POKE_HANDLER)
dispatcher.add_handler(ANAL_HANDLER)
dispatcher.add_handler(HENTAI_HANDLER)
dispatcher.add_handler(AVATAR_HANDLER)
dispatcher.add_handler(EROFEET_HANDLER)
dispatcher.add_handler(HOLO_HANDLER)
dispatcher.add_handler(TITS_HANDLER)
dispatcher.add_handler(PUSSYGIF_HANDLER)
dispatcher.add_handler(HOLOERO_HANDLER)
dispatcher.add_handler(PUSSY_HANDLER)
dispatcher.add_handler(HENTAIGIF_HANDLER)
dispatcher.add_handler(CLASSIC_HANDLER)
dispatcher.add_handler(KUNI_HANDLER)
dispatcher.add_handler(WAIFU_HANDLER)
dispatcher.add_handler(LEWD_HANDLER)
dispatcher.add_handler(KISS_HANDLER)
dispatcher.add_handler(FEMDOM_HANDLER)
dispatcher.add_handler(CUDDLE_HANDLER)
dispatcher.add_handler(EROK_HANDLER)
dispatcher.add_handler(FOXGIRL_HANDLER)
dispatcher.add_handler(TITSGIF_HANDLER)
dispatcher.add_handler(ERO_HANDLER)
dispatcher.add_handler(SMUG_HANDLER)
dispatcher.add_handler(BAKA_HANDLER)
dispatcher.add_handler(DVA_HANDLER)

__handlers__ = [
    NEKO_HANDLER,
    FEET_HANDLER,
    YURI_HANDLER,
    TRAP_HANDLER,
    FUTANARI_HANDLER,
    HOLOLEWD_HANDLER,
    SOLOGIF_HANDLER,
    CUMGIF_HANDLER,
    EROKEMO_HANDLER,
    LESBIAN_HANDLER,
    WALLPAPER_HANDLER,
    LEWDK_HANDLER,
    NGIF_HANDLER,
    TICKLE_HANDLER,
    LEWD_HANDLER,
    FEED_HANDLER,
    EROYURI_HANDLER,
    ERON_HANDLER,
    CUM_HANDLER,
    BJGIF_HANDLER,
    BJ_HANDLER,
    NEKONSFW_HANDLER,
    SOLO_HANDLER,
    KEMONOMIMI_HANDLER,
    AVATARLEWD_HANDLER,
    GASM_HANDLER,
    POKE_HANDLER,
    ANAL_HANDLER,
    HENTAI_HANDLER,
    AVATAR_HANDLER,
    EROFEET_HANDLER,
    HOLO_HANDLER,
    TITS_HANDLER,
    PUSSYGIF_HANDLER,
    HOLOERO_HANDLER,
    PUSSY_HANDLER,
    HENTAIGIF_HANDLER,
    CLASSIC_HANDLER,
    KUNI_HANDLER,
    WAIFU_HANDLER,
    LEWD_HANDLER,
    KISS_HANDLER,
    FEMDOM_HANDLER,
    LEWDKEMO_HANDLER,
    CUDDLE_HANDLER,
    EROK_HANDLER,
    FOXGIRL_HANDLER,
    TITSGIF_HANDLER,
    ERO_HANDLER,
    SMUG_HANDLER,
    BAKA_HANDLER,
    DVA_HANDLER,
]
