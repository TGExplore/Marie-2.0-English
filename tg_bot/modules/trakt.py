from trakt import Trakt
from tg_bot import dispatcher, MESSAGE_DUMP, LOGGER
from tg_bot.modules.disable import DisableAbleCommandHandler
from telegram import ParseMode, Update, Bot
from telegram.ext import run_async
import tmdbsimple as tmdb
import datetime
import requests
from bs4 import BeautifulSoup as BS
import json

tmdb.API_KEY = '44ec5f422b554212fb8bd83da7323142'
Trakt.configuration.defaults.client(
    id="46fa1c789a7e019574e4946af5824546f05e7dece99f5384bfaeb1c0641bb051"
)


@run_async
def tvair(bot: Bot, update: Update):
    KEY = '44ec5f422b554212fb8bd83da7323142'
    res = ""

    def extractdata(file):
        for line in file:
            line = str(line)
            if "calendar :" in line:
                return line

    url = "https://www.tvtime.com/en/calendar"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84"}
    response = requests.get(url, headers=headers)
    data = response.text

    soup = BS(data, 'lxml')
    op = soup.find_all("script", attrs={"type": "text/javascript"})[4]
    data = extractdata(op).split(";", maxsplit=1)[1]
    del op, soup
    data = data.split("=", maxsplit=1)[1]
    data = data.split("'", maxsplit=2)[1]
    data = data.replace("\&quot;", '"')
    data = data.replace("\&#039;", "'")
    data = data.replace(',"', ',\n"')
    data = data.replace("{", " { ")
    data = data.replace("\\\/", "/")
    data = data.replace('\\\\"', '')
    data.strip()
    fop = json.loads(data)

    today = str(datetime.date.today())
    ids = []
    data = []
    for show in fop:
        if show['air_date'] == today:
            data.append(show)
    del fop

    def sfunc(s):
        return s['show']['nb_followers']

    data.sort(reverse=True, key=sfunc)

    for show in data:
        ids.append(show['show']['id'])

    ids = sorted(set(ids), key=lambda x: ids.index(x))
    for id in ids:
        item = Trakt['search'].lookup(id, 'tvdb')[0].to_identifier()
        try:
            res += "[" + str(item['title']) + "](https://t.me/share/url?url=/sinfo%20{sid})".format(
                sid=item['ids']['tmdb']) + " (_"
            try:
                req = requests.get(
                    "https://api.themoviedb.org/3/tv/{tv_id}/watch/providers?api_key={key}".format(
                        tv_id=item['ids']['tmdb'], key=KEY)).json()['results']
                for p in req['IN']['flatrate']:
                    res += p['provider_name']
            except KeyError as e:
                res += "NA"
            res += "_)\n"
        except KeyError:
            pass
    del data, ids
    update.effective_message.reply_text(
        res, parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=False
    )


@run_async
def show(bot: Bot, update: Update):
    message = update.effective_message
    res = ""
    # /sinfo 1234
    sid = message.text[7:]
    show = tmdb.TV(sid)
    info = show.info()

    res += "*Title: {name}* ({year})".format(name=info['name'], year=str(info['first_air_date']).split("-")[0])
    res += "\n_" + info['tagline'] + "_"
    res += "\n*Genres:* "
    for g in info['genres']:
        res += g['name'] + " "
    res += "\n*Overview:* " + info['overview']
    res += "\n\n*Status:* " + info['status']
    res += "\n*Recent Episode:* " + info['last_episode_to_air']['name'] + " (S{s}E{e})".format(
        s=info['last_episode_to_air']['season_number'],
        e=info['last_episode_to_air']['episode_number'])
    if info['status'] != "Ended":
        res += "\n*Next episode:* "
        try:
            res += info['next_episode_to_air']['name'] + " (S{0}E{1}) ".format(
                info['next_episode_to_air']['season_number'],
                info['next_episode_to_air']['episode_number']) + " ({})".format(info['next_episode_to_air']['air_date'])
        except TypeError:
            res += "_NA_"
    res += "\n*Network:* [" + info['networks'][0]['name'] + "]({})".format(info['homepage'])
    res += "\n\n*Recommendations:*"
    recs = show.recommendations()
    recs = recs['results'][:5]
    for r in recs:
        res += "\n" + "[" + r['name'] + "](https://t.me/share/url?url=/show%20{sid})".format(sid=r['id'])

    POSTER = "https://www.themoviedb.org/t/p/original" + info['poster_path']
    del show
    del info
    del recs
    update.effective_message.reply_photo(
        POSTER,
        res, parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )


@run_async
def air(bot: Bot, update: Update):
    KEY = '44ec5f422b554212fb8bd83da7323142'
    res = "*Shows Airing Today:*\n\n"
    tv = tmdb.TV()
    response = []
    for i in range(1, 3):
        try:
            response.append(tv.airing_today(timezone="IST", page=i))
        except:
            res += "Sorry, there's been connection error!\nPlease Try again later (After 15-20 minutes.)"
            break
    data = []
    for i in response:
        for j in i['results']:
            if j['original_language'] in ["en", "hi", "te", "mr", "ta", "ml"]:
                data.append(j)
    del response
    for i in data:
        res += "[" + i['name'] + "](https://t.me/share/url?url=/sinfo%20{sid})".format(sid=i['id']) + " (_"
        try:
            req = requests.get(
                "https://api.themoviedb.org/3/tv/{tv_id}/watch/providers?api_key={key}".format(
                    tv_id=i['id'], key=KEY)).json()['results']
            for p in req['IN']['flatrate']:
                res += p['provider_name']
        except KeyError as e:
            res += "NA"
        res += "_)\n"

    del data
    update.effective_message.reply_text(
        res, parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=False
    )


@run_async
def otv(bot: Bot, update: Update):
    res = "*Ongoing TV Shows*\n\n"
    tv = tmdb.TV()
    KEY = '44ec5f422b554212fb8bd83da7323142'
    response = []
    for i in range(1, 3):
        try:
            response.append(tv.on_the_air(page=i))
        except:
            res += "Sorry, there's been connection error!\nPlease Try again later (After 15-20 minutes.)"
            break
    data = []
    for i in response:
        for j in i['results']:
            if j['original_language'] in ["en", "hi", "te", "mr", "ta", "ml"]:
                data.append(j)
    del response
    for i in data:
        res += "[" + i['name'] + "](https://t.me/share/url?url=/sinfo%20{sid})".format(sid=i['id']) + " (_"
        try:
            req = requests.get(
                "https://api.themoviedb.org/3/tv/{tv_id}/watch/providers?api_key={key}".format(
                    tv_id=i['id'], key=KEY)).json()['results']
            for p in req['IN']['flatrate']:
                res += p['provider_name']
        except KeyError as e:
            res += "NA"
        res += "_)\n"

    del data
    update.effective_message.reply_text(res, parse_mode=ParseMode.MARKDOWN)


@run_async
def umovie(bot: Bot, update: Update):
    res = "*Upcoming Movies:*\n\n"
    mov = tmdb.Movies()
    response = mov.upcoming()
    for j in response['results']:
        if datetime.datetime.strptime(j['release_date'], "%Y-%m-%d") > datetime.datetime.today():
            res += j['title'] + ", " + j['release_date'] + "\n"

    update.effective_message.reply_text(res, parse_mode=ParseMode.MARKDOWN)


@run_async
def trendingm(bot: Bot, update: Update):
    res = "*Trending Movies:*\n\n"
    items = Trakt['movies'].trending()
    for i in range(10):
        res += items[i].title + " (" + str(items[i].year) + ")\n"

    update.effective_message.reply_text(res, parse_mode=ParseMode.MARKDOWN)


@run_async
def trendings(bot: Bot, update: Update):
    res = "*Trending Shows:*\n\n"
    items = Trakt['shows'].trending()
    for i in range(10):
        res += items[i].title + " (" + str(items[i].year) + ")\n"

    update.effective_message.reply_text(res, parse_mode=ParseMode.MARKDOWN)


TVAIR_HANDLER = DisableAbleCommandHandler("tvair", tvair)
dispatcher.add_handler(TVAIR_HANDLER)

SINFO_HANDLER = DisableAbleCommandHandler("sinfo", sinfo)
dispatcher.add_handler(SINFO_HANDLER)

AIR_HANDLER = DisableAbleCommandHandler("air", air)
dispatcher.add_handler(AIR_HANDLER)

OTV_HANDLER = DisableAbleCommandHandler("otv", otv)
dispatcher.add_handler(OTV_HANDLER)

UMOVIE_HANDLER = DisableAbleCommandHandler("umovie", umovie)
dispatcher.add_handler(UMOVIE_HANDLER)

TRENDINGS_HANDLER = DisableAbleCommandHandler("trendings", trendings)
dispatcher.add_handler(TRENDINGS_HANDLER)

TRENDINGM_HANDLER = DisableAbleCommandHandler("trendingm", trendingm)
dispatcher.add_handler(TRENDINGM_HANDLER)
