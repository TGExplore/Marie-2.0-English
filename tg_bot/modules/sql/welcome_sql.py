import threading
from typing import Union
from sqlalchemy import Column, String, Boolean, UnicodeText, Integer, BigInteger

from tg_bot.modules.helper_funcs.msg_types import Types
from tg_bot.modules.sql import SESSION, BASE

DEFAULT_WELCOME = "Hey Welcome {first}, how are you?"
DEFAULT_GOODBYE = "Nice knowing ya!"


class Welcome(BASE):
    __tablename__ = "welcome_pref"
    chat_id = Column(String(14), primary_key=True)
    should_welcome = Column(Boolean, default=True)
    should_goodbye = Column(Boolean, default=True)

    custom_welcome = Column(UnicodeText, default=DEFAULT_WELCOME)
    welcome_type = Column(Integer, default=Types.TEXT.value)

    custom_leave = Column(UnicodeText, default=DEFAULT_GOODBYE)
    leave_type = Column(Integer, default=Types.TEXT.value)

    clean_welcome = Column(BigInteger)
    del_joined = Column(BigInteger)

    def __init__(self, chat_id, should_welcome=True, should_goodbye=True):
        self.chat_id = chat_id
        self.should_welcome = should_welcome
        self.should_goodbye = should_goodbye

    def __repr__(self):
        return "<Chat {} should Welcome new users: {}>".format(self.chat_id, self.should_welcome)

class WelcomeButtons(BASE):
    __tablename__ = "welcome_urls"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(14), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    url = Column(UnicodeText, nullable=False)
    same_line = Column(Boolean, default=False)

    def __init__(self, chat_id, name, url, same_line=False):
        self.chat_id = str(chat_id)
        self.name = name
        self.url = url
        self.same_line = same_line
        
        
class CleanServiceSetting(BASE):
    __tablename__ = "clean_service"
    chat_id = Column(String(14), primary_key=True)
    clean_service = Column(Boolean, default=True)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)

    def __repr__(self):
        return "<Chat used clean service ({})>".format(self.chat_id)
    
    
class GoodbyeButtons(BASE):
    __tablename__ = "leave_urls"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(14), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    url = Column(UnicodeText, nullable=False)
    same_line = Column(Boolean, default=False)

    def __init__(self, chat_id, name, url, same_line=False):
        self.chat_id = str(chat_id)
        self.name = name
        self.url = url
        self.same_line = same_line

class WelcomeSecurity(BASE):
    __tablename__ = "welcome_security"
    chat_id = Column(String(14), primary_key=True)
    security = Column(UnicodeText)

    def __init__(self, chat_id, security):
        self.chat_id = str(chat_id) # ensure string
        self.security = security

class CombotCASStatus(BASE):
    __tablename__ = "cas_stats"
    chat_id = Column(String(14), primary_key=True)
    status = Column(Boolean, default=True)
    autoban = Column(Boolean, default=False)
    
    def __init__(self, chat_id, status, autoban):
        self.chat_id = str(chat_id) #chat_id is int, make sure it's string
        self.status = status
        self.autoban = autoban

class BannedChat(BASE):
    __tablename__ = "chat_blacklists"
    chat_id = Column(String(14), primary_key=True)
    
    def __init__(self, chat_id):
        self.chat_id = str(chat_id) #chat_id is int, make sure it is string

class DefenseMode(BASE):
    __tablename__ = "defense_mode"
    chat_id = Column(String(14), primary_key=True)
    status = Column(Boolean, default=False)
    
    def __init__(self, chat_id, status):
        self.chat_id = str(chat_id)
        self.status = status

class AutoKickSafeMode(BASE):
    __tablename__ = "autokicks_safemode"
    chat_id = Column(String(14), primary_key=True)
    timeK = Column(Integer, default=90)
    
    def __init__(self, chat_id, timeK):
        self.chat_id = str(chat_id)
        self.timeK = timeK

Welcome.__table__.create(checkfirst=True)
WelcomeButtons.__table__.create(checkfirst=True)
GoodbyeButtons.__table__.create(checkfirst=True)
WelcomeSecurity.__table__.create(checkfirst=True)
CombotCASStatus.__table__.create(checkfirst=True)
BannedChat.__table__.create(checkfirst=True)
DefenseMode.__table__.create(checkfirst=True)
AutoKickSafeMode.__table__.create(checkfirst=True)


INSERTION_LOCK = threading.RLock()
WELC_BTN_LOCK = threading.RLock()
LEAVE_BTN_LOCK = threading.RLock()
WS_LOCK = threading.RLock()
CAS_LOCK = threading.RLock()
BANCHATLOCK = threading.RLock()
DEFENSE_LOCK = threading.RLock()
AUTOKICK_LOCK = threading.RLock()

BLACKLIST = set()

def welcome_security(chat_id):
    try:
        security = SESSION.query(WelcomeSecurity).get(str(chat_id))
        if security:
            return security.security
        return False
    finally:
        SESSION.close()


def set_welcome_security(chat_id, security):
    with WS_LOCK:
        prev = SESSION.query(WelcomeSecurity).get((str(chat_id)))
        if prev:
            SESSION.delete(prev)
        welcome_s = WelcomeSecurity(str(chat_id), security)
        SESSION.add(welcome_s)
        SESSION.commit()
        
def get_welc_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()
    if welc:
        return welc.should_welcome, welc.custom_welcome, welc.welcome_type
    else:
        # Welcome by default.
        return True, DEFAULT_WELCOME, Types.TEXT

def get_welc_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()
    if welc:
        return welc.should_welcome, welc.custom_welcome, welc.welcome_type
    else:
        # Welcome by default.
        return True, DEFAULT_WELCOME, Types.TEXT

def get_gdbye_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()
    if welc:
        return welc.should_goodbye, welc.custom_leave, welc.leave_type
    else:
        # Welcome by default.
        return True, DEFAULT_GOODBYE, Types.TEXT

def set_clean_welcome(chat_id, clean_welcome):
    with INSERTION_LOCK:
        curr = SESSION.query(Welcome).get(str(chat_id))
        if not curr:
            curr = Welcome(str(chat_id))

        curr.clean_welcome = int(clean_welcome)

        SESSION.add(curr)
        SESSION.commit()

def get_clean_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()

    if welc:
        return welc.clean_welcome

    return False

def set_del_joined(chat_id, del_joined):
    with INSERTION_LOCK:
        curr = SESSION.query(Welcome).get(str(chat_id))
        if not curr:
            curr = Welcome(str(chat_id))

        curr.del_joined = int(del_joined)

        SESSION.add(curr)
        SESSION.commit()

def get_del_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()

    if welc:
        return welc.del_joined

    return False

def set_welc_preference(chat_id, should_welcome):
    with INSERTION_LOCK:
        curr = SESSION.query(Welcome).get(str(chat_id))
        if not curr:
            curr = Welcome(str(chat_id), should_welcome=should_welcome)
        else:
            curr.should_welcome = should_welcome

        SESSION.add(curr)
        SESSION.commit()

def set_gdbye_preference(chat_id, should_goodbye):
    with INSERTION_LOCK:
        curr = SESSION.query(Welcome).get(str(chat_id))
        if not curr:
            curr = Welcome(str(chat_id), should_goodbye=should_goodbye)
        else:
            curr.should_goodbye = should_goodbye

        SESSION.add(curr)
        SESSION.commit()

def set_custom_welcome(chat_id, custom_welcome, welcome_type, buttons=None):
    if buttons is None:
        buttons = []

    with INSERTION_LOCK:
        welcome_settings = SESSION.query(Welcome).get(str(chat_id))
        if not welcome_settings:
            welcome_settings = Welcome(str(chat_id), True)

        if custom_welcome:
            welcome_settings.custom_welcome = custom_welcome
            welcome_settings.welcome_type = welcome_type.value

        else:
            welcome_settings.custom_welcome = DEFAULT_GOODBYE
            welcome_settings.welcome_type = Types.TEXT.value

        SESSION.add(welcome_settings)

        with WELC_BTN_LOCK:
            prev_buttons = SESSION.query(WelcomeButtons).filter(WelcomeButtons.chat_id == str(chat_id)).all()
            for btn in prev_buttons:
                SESSION.delete(btn)

            for b_name, url, same_line in buttons:
                button = WelcomeButtons(chat_id, b_name, url, same_line)
                SESSION.add(button)

        SESSION.commit()


def get_custom_welcome(chat_id):
    welcome_settings = SESSION.query(Welcome).get(str(chat_id))
    ret = DEFAULT_WELCOME
    if welcome_settings and welcome_settings.custom_welcome:
        ret = welcome_settings.custom_welcome

    SESSION.close()
    return ret

def set_custom_gdbye(chat_id, custom_goodbye, goodbye_type, buttons=None):
    if buttons is None:
        buttons = []

    with INSERTION_LOCK:
        welcome_settings = SESSION.query(Welcome).get(str(chat_id))
        if not welcome_settings:
            welcome_settings = Welcome(str(chat_id), True)

        if custom_goodbye:
            welcome_settings.custom_leave = custom_goodbye
            welcome_settings.leave_type = goodbye_type.value

        else:
            welcome_settings.custom_leave = DEFAULT_GOODBYE
            welcome_settings.leave_type = Types.TEXT.value

        SESSION.add(welcome_settings)

        with LEAVE_BTN_LOCK:
            prev_buttons = SESSION.query(GoodbyeButtons).filter(GoodbyeButtons.chat_id == str(chat_id)).all()
            for btn in prev_buttons:
                SESSION.delete(btn)

            for b_name, url, same_line in buttons:
                button = GoodbyeButtons(chat_id, b_name, url, same_line)
                SESSION.add(button)

        SESSION.commit()

def get_custom_gdbye(chat_id):
    welcome_settings = SESSION.query(Welcome).get(str(chat_id))
    ret = DEFAULT_GOODBYE
    if welcome_settings and welcome_settings.custom_leave:
        ret = welcome_settings.custom_leave

    SESSION.close()
    return ret

def get_welc_buttons(chat_id):
    try:
        return SESSION.query(WelcomeButtons).filter(WelcomeButtons.chat_id == str(chat_id)).order_by(
            WelcomeButtons.id).all()
    finally:
        SESSION.close()

def get_gdbye_buttons(chat_id):
    try:
        return SESSION.query(GoodbyeButtons).filter(GoodbyeButtons.chat_id == str(chat_id)).order_by(
            GoodbyeButtons.id).all()
    finally:
        SESSION.close()

def get_cas_status(chat_id):
    try:
        resultObj = SESSION.query(CombotCASStatus).get(str(chat_id))
        if resultObj:
            return resultObj.status
        return True
    finally:
        SESSION.close()

def set_cas_status(chat_id, status):
    with CAS_LOCK:
        ban = False
        prevObj = SESSION.query(CombotCASStatus).get(str(chat_id))
        if prevObj:
            ban = prevObj.autoban
            SESSION.delete(prevObj)
        newObj = CombotCASStatus(str(chat_id), status, ban)
        SESSION.add(newObj)
        SESSION.commit()

def get_cas_autoban(chat_id):
    try:
        resultObj = SESSION.query(CombotCASStatus).get(str(chat_id))
        if resultObj and resultObj.autoban:
            return resultObj.autoban
        return False
    finally:
        SESSION.close()
        
def set_cas_autoban(chat_id, autoban):
    with CAS_LOCK:
        status = True
        prevObj = SESSION.query(CombotCASStatus).get(str(chat_id))
        if prevObj:
            status = prevObj.status
            SESSION.delete(prevObj)
        newObj = CombotCASStatus(str(chat_id), status, autoban)
        SESSION.add(newObj)
        SESSION.commit()

def migrate_chat(old_chat_id, new_chat_id):
    with INSERTION_LOCK:
        chat = SESSION.query(Welcome).get(str(old_chat_id))
        if chat:
            chat.chat_id = str(new_chat_id)

        with WELC_BTN_LOCK:
            chat_buttons = SESSION.query(WelcomeButtons).filter(WelcomeButtons.chat_id == str(old_chat_id)).all()
            for btn in chat_buttons:
                btn.chat_id = str(new_chat_id)

        with LEAVE_BTN_LOCK:
            chat_buttons = SESSION.query(GoodbyeButtons).filter(GoodbyeButtons.chat_id == str(old_chat_id)).all()
            for btn in chat_buttons:
                btn.chat_id = str(new_chat_id)

        SESSION.commit()

def __load_blacklisted_chats_list(): #load shit to memory to be faster, and reduce disk access 
    global BLACKLIST
    try:
        BLACKLIST = {x.chat_id for x in SESSION.query(BannedChat).all()}
    finally:
        SESSION.close()


def isBanned(chat_id):
    return chat_id in BLACKLIST

def getDefenseStatus(chat_id):
    try:
        resultObj = SESSION.query(DefenseMode).get(str(chat_id))
        if resultObj:
            return resultObj.status
        return False #default
    finally:
        SESSION.close()

def setDefenseStatus(chat_id, status):
    with DEFENSE_LOCK:
        prevObj = SESSION.query(DefenseMode).get(str(chat_id))
        if prevObj:
            SESSION.delete(prevObj)
        newObj = DefenseMode(str(chat_id), status)
        SESSION.add(newObj)
        SESSION.commit()

def getKickTime(chat_id):
    try:
        resultObj = SESSION.query(AutoKickSafeMode).get(str(chat_id))
        if resultObj:
            return resultObj.timeK
        return 90 #90 seconds
    finally:
        SESSION.close()

def setKickTime(chat_id, value):
    with AUTOKICK_LOCK:
        prevObj = SESSION.query(AutoKickSafeMode).get(str(chat_id))
        if prevObj:
            SESSION.delete(prevObj)
        newObj = AutoKickSafeMode(str(chat_id), int(value))
        SESSION.add(newObj)
        SESSION.commit()

def clean_service(chat_id: Union[str, int]) -> bool:
    try:
        chat_setting = SESSION.query(CleanServiceSetting).get(str(chat_id))
        if chat_setting:
            return chat_setting.clean_service
        return False
    finally:
        SESSION.close()


def set_clean_service(chat_id: Union[int, str], setting: bool):
    with CS_LOCK:
        chat_setting = SESSION.query(CleanServiceSetting).get(str(chat_id))
        if not chat_setting:
            chat_setting = CleanServiceSetting(chat_id)

        chat_setting.clean_service = setting
        SESSION.add(chat_setting)
        SESSION.commit()
        
__load_blacklisted_chats_list()
