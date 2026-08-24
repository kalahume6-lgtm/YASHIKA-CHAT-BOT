from os import getenv
from dotenv import load_dotenv

load_dotenv()


def _get_int(key: str, default=None):
    value = getenv(key)
    if value is None or str(value).strip() == "":
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


# Required
API_ID = _get_int("API_ID")
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN")
OWNER_ID = _get_int("OWNER_ID")

# Optional
SUPPORT_GRP = getenv("SUPPORT_GRP", "")
UPDATE_CHNL = getenv("UPDATE_CHNL", "")
OWNER_USERNAME = getenv("OWNER_USERNAME", "")

# Hosting
PORT = _get_int("PORT", 10000)

# SQLite DB path (No MongoDB / No external DB needed)
DB_PATH = getenv("DB_PATH", "data/bot.db")
