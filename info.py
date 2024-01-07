import re, os
from os import environ
from Script import script 

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ.get('API_ID', '22301351'))
API_HASH = environ.get('API_HASH', '3035f2bbd92a9c5174d174d92b52b25b')
BOT_TOKEN = environ.get('BOT_TOKEN', "6840063368:AAGs0Yd9bg6i9WmhL-hvym1gOxMqGDXi278")

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))

PICS = (environ.get('PICS', 'https://telegra.ph/file/1f782c4fa53ee300e1dfa.jpg')).split()
NOR_IMG = environ.get("NOR_IMG", "https://graph.org/file/e9d4fcb45ed02f1ba5147.jpg")
SPELL_IMG = environ.get("SPELL_IMG", "https://graph.org/file/b8577b96d9fdae40c971b.jpg")
PICS_1 = (environ.get('PICS_1' ,'https://graph.org/file/d2c20ed467fd8a101409f.jpg https://graph.org/file/9fbfa93142640fdaeaf80.jpg https://graph.org/file/e2fba097d69d27061b1e1.jpg https://graph.org/file/fed816c138a42cafc24bb.jpg https://graph.org/file/e6ecfe9f99030aebbbd05.jpg https://graph.org/file/941bae7b0584a16eb0fd2.jpg https://graph.org/file/3f38fa53398771d450c0f.jpg')).split()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '5721673207').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1001859046902 -1002108230565').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
PREMIUM_USER = [int(user) if id_pattern.search(user) else user for user in environ.get('PREMIUM_USER', '5721673207').split()]
auth_channel = environ.get('AUTH_CHANNEL', '')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None

fsuboff = environ.get('FSUBOFF')
FSUBOFF = int(fsuboff) if fsuboff and id_pattern.search(fsuboff) else None

AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None
support_chat_id = environ.get('SUPPORT_CHAT_ID', '')
reqst_channel = environ.get('REQST_CHANNEL', '-1002072344938')
REQST_CHANNEL = int(reqst_channel) if reqst_channel and id_pattern.search(reqst_channel) else None
SUPPORT_CHAT_ID = int(support_chat_id) if support_chat_id and id_pattern.search(support_chat_id) else None
NO_RESULTS_MSG = bool(environ.get("NO_RESULTS_MSG", False))
PREMIUM_LOGS = int(environ.get('PREMIUM_LOGS', '-1002072344938'))
USERNAME = environ.get('USERNAME', 'https://t.me/AkshayChand08')

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://akshaychand:akshaychand@cluster0.3gwaqm0.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME = environ.get('DATABASE_NAME', "OnlineTube")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

# Others
VERIFY = bool(environ.get('VERIFY', True))
IS_SHORTLINK = is_enabled(environ.get("IS_SHORTLINK", "False"), True)
SHORTLINK_URL = environ.get('SHORTLINK_URL', 'earn2me.com')
SHORTLINK_API = environ.get('SHORTLINK_API', '9c65da040c06369120fe6487c3f72406c59047b7')
#SECOND_SHORTLINK_URL = environ.get('SECOND_SHORTLINK_URL', 'mdiskshortner.link')
#SECOND_SHORTLINK_API = environ.get('SECOND_SHORTLINK_API', 'fc6297ad0ad340ec66c75ce9157e056176bd7a81')
SECOND_SHORTLINK_URL = environ.get('SECOND_SHORTLINK_URL', None)
SECOND_SHORTLINK_API = environ.get('SECOND_SHORTLINK_API', None)
ALL_SHORT_LINK_OFF = is_enabled(environ.get("ALL_SHORT_LINK_OFF", "False"), False)


MAX_B_TN = environ.get("MAX_B_TN", "6")
MAX_BTN = is_enabled((environ.get('MAX_BTN', "True")), True)
PORT = environ.get("PORT", "8080")
GRP_LNK = environ.get('GRP_LNK', 'https://t.me/iPapcornPrimeGroup')
CHNL_LNK = environ.get('CHNL_LNK', 'https://t.me/arsOfficial10')
TUTORIAL = environ.get('TUTORIAL', 'https://t.me/HoW_ToOpEn/42')
IS_TUTORIAL = bool(environ.get('IS_TUTORIAL', True))
MSG_ALRT = environ.get('MSG_ALRT', 'Wʜᴀᴛ Aʀᴇ Yᴏᴜ Lᴏᴏᴋɪɴɢ Aᴛ ?')
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002072344938'))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', '+r9ArDaaCETE0OGU9')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "False")), False)
IMDB = is_enabled((environ.get('IMDB', "False")), False)
AUTO_FFILTER = is_enabled((environ.get('AUTO_FFILTER', "True")), True)
AUTO_DELETE = is_enabled((environ.get('AUTO_DELETE', "True")), True)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CAPTION}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", f"{script.IMDB_TEMPLATE_TXT}")
WELCOME_TEXT = environ.get("WELCOME_TEXT", f"{script.WELCOME_TEXT}")

LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '-1001627590692')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "False")), False)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)


#this vars for online streaming code

BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", "-1001558291173")) 
GEN_URL = os.environ.get("DIRECT_GEN_URL", "http://filestreambot-21yk.onrender.com/") # https://example.com/


LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two separate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as different buttons\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"Your current IMDB template is {IMDB_TEMPLATE}"

#verify 

#bot owner 
SHORTENER_API = environ.get("SHORTENER_API", "9c65da040c06369120fe6487c3f72406c59047b7")
SHORTENER_WEBSITE = environ.get("SHORTENER_WEBSITE", "earn2me.com")
#SHORTENER_API2 = environ.get("SHORTENER_API2", "6ee7840bdaf0103a11214c62c8b0a5d05fe347c3")
#SHORTENER_WEBSITE2 = environ.get("SHORTENER_WEBSITE2", "tnshort.net")
SHORTENER_API2 = environ.get("SHORTENER_API2", None)
SHORTENER_WEBSITE2 = environ.get("SHORTENER_WEBSITE2", None)


SHORT_URL = is_enabled((environ.get('SHORT_URL', "True")), True)
IS_VERIFY = bool(environ.get('IS_VERIFY', True))


#bot user
TUTORIAL_LINK_1 = os.environ.get('TUTORIAL_LINK_1', None)
TUTORIAL_LINK_2 = os.environ.get('TUTORIAL_LINK_2', None)
#TUTORIAL_LINK_1 = os.environ.get('TUTORIAL_LINK_1', 'https://t.me/howtodownload91/44')

VERIFY_IMG = environ.get("VERIFY_IMG", "https://telegra.ph/file/42d79197597d79418d438.jpg")
VERIFY_LOG = int(environ.get('VERIFY_LOG', '-1002072344938'))

SHORTLINK_URL = environ.get("SHORTLINK_URL", None)
SHORTLINK_API = environ.get("SHORTLINK_API", None)
SHORTLINK_API2 = environ.get("SHORTLINK_API2", None)
SHORTLINK_URL2 = environ.get("SHORTLINK_URL2", None)

#SHORTLINK_API = environ.get("SHORTLINK_API", "9c65da040c06369120fe6487c3f72406c59047b7")
#SHORTLINK_URL = environ.get("SHORTLINK_URL", "earn2me.com")
#SHORTLINK_API2 = environ.get("SHORTLINK_API2", "9c65da040c06369120fe6487c3f72406c59047b7")
#SHORTLINK_URL2 = environ.get("SHORTLINK_URL2", "earn2me.com")






VERIFY_1_SHORTENERS = environ.get("VERIFY_1_SHORTENERS", "")

VERIFY_1_SHORTENERS = [(data.split(",")[0].strip(), data.split(",")[1].strip()) for data in VERIFY_1_SHORTENERS.splitlines()]

#add custom shorter

VERIFY_1_SHORTENERS=[("9c65da040c06369120fe6487c3f72406c59047b7", "earn2me.com")]


#nremove wrong words

REPLACE_WORDS = (
    list(os.environ.get("REPLACE_WORDS").split(","))
    if os.environ.get("REPLACE_WORDS")
    else []
)

REPLACE_WORDS=["movies", "Movies", ",", "episode", "Episode", "episodes", "Episodes", "south indian", "South Indian", "web-series", "punjabi", "marathi", "gujrati", "combined", "!", "kro", "jaldi", "bhai", "Audio", "audio", "movi", "language", "Language", "Hollywood", "All", "all", "bollywood", "Bollywood", "South", "south", "hd", "karo", "Karo", "fullepisode", "please", "plz", "Please", "Plz", "send", "link", "Link", "#request", ":", "'", "full", "Full", "movie", "Movie", "dubb", "dabbed", "dubbed", "gujarati", "season", "Season", "web", "series", "Web", "Series", "webseries", "WebSeries", "upload", "HD", "Hd", "bhejo", "ful", "Send", "Bhejo"]
