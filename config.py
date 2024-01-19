import os

from dotenv import load_dotenv

load_dotenv()


DB_URL = os.getenv("DB_URL")
DB_URL_TEST = os.getenv("DB_URL_TEST")
APIKEY = os.getenv("APIKEY")
USER_ID = os.getenv("USER_ID")
REDIS_URL = os.getenv("REDIS_URL")
LOG_LEVEL = os.getenv("LOG_LEVEL")
LOG_FILE = os.getenv("LOG_FILE")
LOG_FORMAT = os.getenv("LOG_FORMAT")

TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

DEPRECIATION_FACTOR = float(os.getenv("DEPRECIATION_FACTOR"))
INCREASE_FACTOR = float(os.getenv("INCREASE_FACTOR"))
ITEMS_ON_PAGE = int(os.getenv("ITEMS_ON_PAGE"))
TOP_ITEMS_AMOUNT = int(os.getenv("TOP_ITEMS_AMOUNT"))
ITEMS_LIMIT = int(os.getenv("ITEMS_LIMIT"))
STORAGE_TIME = int(os.getenv("STORAGE_TIME"))
SCHEDULE_INTERVAL = int(os.getenv("SCHEDULE_INTERVAL"))
START_RANGE_SLEEP = int(os.getenv("START_RANGE_SLEEP"))
STOP_RANGE_SLEEP = int(os.getenv("STOP_RANGE_SLEEP"))
ERROR_STORAGE_TIME = int(os.getenv("ERROR_STORAGE_TIME"))
REPEAT_AFTER_ERROR_TIME = int(os.getenv("REPEAT_AFTER_ERROR_TIME"))
FLOATING_POINT_VARIABLE = int(os.getenv("FLOATING_POINT_VARIABLE"))
"""
Symbols of popular currencies:
https://partner.steamgames.com/doc/store/pricing/currencies
"""
CURRENCY = int(os.getenv("CURRENCY"))

URL_FOR_STEAM_GAME = os.getenv("URL_FOR_STEAM_GAME")
URL_FOR_STEAM_ITEM = os.getenv("URL_FOR_STEAM_ITEM")
