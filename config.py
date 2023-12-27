import os

from dotenv import load_dotenv

load_dotenv()


DB_URL = os.getenv("DB_URL")
APIKEY = os.getenv("APIKEY")
USER_ID = os.getenv("USER_ID")
REDIS_URL = os.getenv("REDIS_URL")


TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

DEPRECIATION_FACTOR = float(os.getenv("DEPRECIATION_FACTOR"))
INCREASE_FACTOR = float(os.getenv("INCREASE_FACTOR"))
ITEMS_ON_PAGE = int(os.getenv("ITEMS_ON_PAGE"))

URL_FOR_STEAM_GAME = os.getenv("URL_FOR_STEAM_GAME")
URL_FOR_STEAM_ITEM = os.getenv("URL_FOR_STEAM_ITEM")
