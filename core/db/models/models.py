from sqlalchemy import Column, ForeignKey, Integer, BigInteger, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, relationship


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True)


class User(Base):
    user_name = Column(String, nullable=True)
    telegram_id = Column(Integer, nullable=False, unique=True)

    steam_ids = relationship("SteamId", back_populates="user")

    def __repr__(self):
        return f"{self.__class__.__name__}, name: {self.user_name}, telegram_id: {self.telegram_id}"


class SteamId(Base):
    steam_id = Column(BigInteger)
    steam_name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="steam_ids")
    games = relationship("Game", back_populates="steamid", passive_deletes=True)
    steam_inventorys = relationship(
        "SteamInventory", back_populates="steamid", passive_deletes=True
    )

    def __repr__(self):
        return f"{self.__class__.__name__}, steam_id: {self.steam_id}"


class Game(Base):
    game_name = Column(String)
    game_id = Column(Integer)
    game_cost = Column(Integer)
    time_in_game = Column(Integer)
    steam_id = Column(Integer, ForeignKey("steamids.id", ondelete="CASCADE"))

    steamid = relationship("SteamId", back_populates="games")

    def __repr__(self):
        return f"{self.__class__.__name__}, item_id: {self.game_name}, amount: {self.game_cost}"


class SteamInventory(Base):
    games_id = Column(Integer, nullable=False)
    first_inventory_cost = Column(Integer, default=0, nullable=False)
    inventory_cost = Column(Integer, default=0, nullable=False)
    steam_id = Column(Integer, ForeignKey("steamids.id", ondelete="CASCADE"))

    steamid = relationship("SteamId", back_populates="steam_inventorys")
    items_in = relationship(
        "SteamItemsInInventory", back_populates="steam_inventorys", passive_deletes=True
    )
    # items_in = relationship(
    #     "SteamItem",
    #     secondary="steam_items_in_inventory",
    #     back_populates="steam_inventory",
    # )

    def __repr__(self):
        return f"{self.__class__.__name__}, games_id: {self.games_id}, cost: {self.inventory_cost}"


class SteamItemsInInventory(Base):
    amount = Column(Integer)
    inventory_id = Column(Integer, ForeignKey("steaminventorys.id", ondelete="CASCADE"))
    item_id = Column(
        BigInteger, ForeignKey("steamitems.classid", ondelete="CASCADE"), unique=True
    )

    steam_inventorys = relationship("SteamInventory", back_populates="items_in")
    steam_item = relationship("SteamItem", back_populates="items_in", uselist=False)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}, item_id: {self.item_id}, amount: {self.amount}"
        )


class SteamItem(Base):
    name = Column(String, nullable=False)
    app_id = Column(Integer, nullable=False)
    classid = Column(BigInteger, nullable=False, unique=True)
    first_item_cost = Column(Integer, default=0, nullable=False)
    item_cost = Column(Integer, nullable=False)

    items_in = relationship(
        "SteamItemsInInventory", back_populates="steam_item", passive_deletes=True
    )

    # steam_inventory = relationship(
    #     #     "SteamInventory",
    #     #     secondary="steam_items_in_inventory",
    #     #     back_populates="items_in",
    #     # )

    def __repr__(self):
        return f"{self.__class__.__name__}, classid: {self.classid}, cost: {self.item_cost}"