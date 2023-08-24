from database import engine
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=True)
    telegram_id = Column(Integer, nullable=False, unique=True)
    # steam_id = Column(Integer, nullable=False)

    steam_id = relationship('SteamId', back_populates='user')

    def __repr__(self):
        return f"{self.__class__.__name__}, name: {self.user_name}, telegram_id: {self.telegram_id}"


class SteamId(Base):
    __tablename__ = 'steamids'

    id = Column(Integer, primary_key=True)
    steam_id = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='steamids')
    steaminventory = relationship('SteamInventory', back_populates='steamids')

    def __repr__(self):
        return f"{self.__class__.__name__}, steam_id: {self.steam_id}"


class SteamInventory(Base):
    __tablename__ = 'steam_inventorys'

    id = Column(Integer, primary_key=True)
    games_id = Column(Integer, nullable=False)
    previous_inventory_cost = Column(Integer, default=0, nullable=False)
    now_inventory_cost = Column(Integer, nullable=False)

    # items_quantity = Column(Integer, nullable=False)
    # average_cost = Column(Integer, nullable=False)
    # most_expensive_item = Column(Integer, nullable=False)
    # most_cheaper_item = Column(Integer, nullable=False)

    steam_id = Column(Integer(), ForeignKey('steamids.id'))

    steamid = relationship('SteamId', back_populates='steam_inventorys')
    items_in = relationship("SteamItemsInInventory",
                            secondary="steam_items_in_inventory",
                            back_populates="steam_inventorys")

    def __repr__(self):
        return f"{self.__class__.__name__}, games_id: {self.games_id}, cost: {self.now_inventory_cost}"


class SteamItem(Base):
    __tablename__ = 'steam_items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    app_id = Column(Integer, nullable=False)
    classid = Column(Integer, nullable=False)
    previous_item_cost = Column(Integer, default=0, nullable=False)
    now_item_cost = Column(Integer, nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}, classid: {self.classid}, cost: {self.now_item_cost}"


class SteamItemsInInventory(Base):
    __tablename__ = 'steam_items_in_inventory'

    id = Column(Integer(), primary_key=True)
    amount = Column(SmallInteger())
    inventory_id = Column(Integer(), ForeignKey('steam_inventorys.id'))
    item_id = Column(Integer(), ForeignKey('steam_items.id'))

    def __repr__(self):
        return f"{self.__class__.__name__}, item_id: {self.item_id}, amount: {self.amount}"


Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)
