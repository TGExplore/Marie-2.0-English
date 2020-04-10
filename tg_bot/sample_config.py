# Create a new config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = "True"

    # REQUIRED
    API_KEY = ""
    OWNER_ID = "" # If you dont know, run the bot and do /id in your private chat with it
    OWNER_USERNAME = ""

    # RECOMMENDED
    MESSAGE_DUMP = "None"  # needed to make sure 'save from' messages persist
    LOAD = []
    NO_LOAD = ['translation', 'rss']

    # OPTIONAL
    SUDO_USERS = []  # List of id's (not usernames) for users which have sudo access to the bot.
    SUPPORT_USERS = []  # List of id's (not usernames) for users which are allowed to gban, but can also be banned.
    WHITELIST_USERS = []  # List of id's (not usernames) for users which WONT be banned/kicked by the bot.
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
