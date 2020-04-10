# Create a new config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = "True"

    # REQUIRED
    API_KEY = "1203217513:AAFbw0a6gCekhTGVWmPE0l8SsAMWF1Tc5cI"
    OWNER_ID = "1142196004" # If you dont know, run the bot and do /id in your private chat with it
    OWNER_USERNAME = "loopsword"

    # RECOMMENDED
    MESSAGE_DUMP = "None"  # needed to make sure 'save from' messages persist
    LOAD = []
    NO_LOAD = ['translation', 'rss']

    # OPTIONAL
    SUDO_USERS = [1142196004 722278787 805491896 666670963]  # List of id's (not usernames) for users which have sudo access to the bot.
    SUPPORT_USERS = [1142196004 722278787 805491896 758233009 666670963 955227320]  # List of id's (not usernames) for users which are allowed to gban, but can also be banned.
    WHITELIST_USERS = [1142196004 722278787 805491896 758233009 666670963]  # List of id's (not usernames) for users which WONT be banned/kicked by the bot.
    DONATION_LINK = "None"  # EG, paypal
    CERT_PATH = "None"
    DEL_CMDS = "False"  # Whether or not you should delete "blue text must click" commands
    STRICT_GBAN = "True"
    BAN_STICKER = 'CAADAgADOwADPPEcAXkko5EB3YGYAg'  # banhammer marie sticker
    ALLOW_EXCL = "False"  # Allow ! commands as well as /


class Production(Config):
    LOGGER = "False"


class Development(Config):
    LOGGER = "True"
