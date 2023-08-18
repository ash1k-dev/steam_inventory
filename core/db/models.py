from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    # id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=True)
    telegram_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    steam_id = Column(Integer, nullable=False)
    steam_inventory = relationship('SteamInventory')


class SteamInventory(Base):
    __tablename__ = 'steaminventorys'
    id = Column(Integer)
    previous_inventory_cost = Column(Integer, default=0, nullable=False)
    now_inventory_cost = Column(Integer, nullable=False)
    items_quantity = Column(Integer, nullable=False)
    average_cost = Column(Integer, nullable=False)
    most_expensive_item = Column(Integer, nullable=False)
    most_cheaper_item = Column(Integer, nullable=False)
    user_id = Column(Integer(), ForeignKey('users.user_name'))
    steam_items = relationship('SteamItems')


class SteamItems():
    __tablename__ = 'steamitems'
    name = Column(String, nullable=False)
    app_id = Column(Integer, nullable=False)
    classid = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    previous_item_cost = Column(Integer, default=0, nullable=False)
    now_item_cost = Column(Integer, nullable=False)
    steam_inventory = Column(Integer(), ForeignKey('steaminventorys.id'))