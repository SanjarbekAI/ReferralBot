from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

CHANNELS = [
    ("https://t.me/MyBotTestChannelLink", -1001961644956, "20 KG gacha ozish")
]


DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")
DB_NAME = env.str("DB_NAME")

I18N_DOMAIN = 'lang'
LOCALES_DIR = 'locale'

SHARING_CONSTANT = "https://t.me/sanjarbek_tursunov_bot?start="