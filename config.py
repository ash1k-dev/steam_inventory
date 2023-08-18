import os

from dotenv import load_dotenv

load_dotenv()


DB_URL = os.getenv("DB_URL")
APIKEY = os.getenv("APIKEY")
USER_ID = os.getenv("USER_ID")


TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")


