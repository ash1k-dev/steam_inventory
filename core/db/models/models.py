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
    tracking_items = relationship("ItemTrack", back_populates="user")
    tracking_games = relationship("GameTrack", back_populates="user")


# Steam
class SteamId(Base):
    steam_id = Column(BigInteger)
    steam_name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="steam_ids")
    games = relationship(
        "GameInAccount", back_populates="steamid", passive_deletes=True
    )
    steam_inventorys = relationship(
        "SteamInventory", back_populates="steamid", passive_deletes=True
    )


class Game(Base):
    game_name = Column(String)
    game_id = Column(Integer, nullable=False, unique=True)
    game_cost = Column(Integer)

    games_in = relationship(
        "GameInAccount", back_populates="game", passive_deletes=True
    )


class GameInAccount(Base):
    game_name = Column(String)
    first_game_cost = Column(Integer)
    time_in_game = Column(Integer)
    steam_id = Column(BigInteger, ForeignKey("steamids.id", ondelete="CASCADE"))
    game_id = Column(Integer, ForeignKey("games.game_id", ondelete="CASCADE"))

    steamid = relationship("SteamId", back_populates="games")
    game = relationship(
        "Game",
        back_populates="games_in",
        uselist=False,
    )


class SteamInventory(Base):
    games_id = Column(Integer, nullable=False)
    first_inventory_cost = Column(Integer, default=0, nullable=False)
    inventory_cost = Column(Integer, default=0, nullable=False)
    steam_id = Column(BigInteger, ForeignKey("steamids.id", ondelete="CASCADE"))

    steamid = relationship("SteamId", back_populates="steam_inventorys")
    items_in = relationship(
        "SteamItemsInInventory", back_populates="steam_inventorys", passive_deletes=True
    )


class SteamItemsInInventory(Base):
    amount = Column(Integer)
    first_item_cost = Column(Integer, default=0, nullable=False)
    inventory_id = Column(Integer, ForeignKey("steaminventorys.id", ondelete="CASCADE"))
    item_id = Column(BigInteger, ForeignKey("steamitems.classid", ondelete="CASCADE"))

    steam_inventorys = relationship("SteamInventory", back_populates="items_in")
    steam_item = relationship(
        "SteamItem",
        back_populates="items_in",
        uselist=False,
    )


class SteamItem(Base):
    name = Column(String, nullable=False)
    app_id = Column(Integer, default=730, nullable=False)
    classid = Column(BigInteger, nullable=False, unique=True)
    item_cost = Column(Integer, nullable=False)

    items_in = relationship(
        "SteamItemsInInventory", back_populates="steam_item", passive_deletes=True
    )


class ItemTrack(Base):
    name = Column(String, nullable=False)
    first_item_cost = Column(Integer, default=0, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    item_id = Column(BigInteger, ForeignKey("steamitems.classid", ondelete="CASCADE"))

    user = relationship("User", back_populates="tracking_items")


class GameTrack(Base):
    name = Column(String, nullable=False)
    first_game_cost = Column(Integer, default=0, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    game_id = Column(Integer, ForeignKey("games.game_id", ondelete="CASCADE"))

    user = relationship("User", back_populates="tracking_games")
