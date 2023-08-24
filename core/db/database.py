from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import DB_URL

engine = create_engine(DB_URL, echo = True)

session = Session(bind=engine)