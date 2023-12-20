from sqlalchemy import Column, ForeignKey, Integer, BigInteger, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, relationship


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True)


class User(Base):
    name = Column(String, nullable=True)
    telegram_id = Column(Integer, nullable=False, unique=True)

    steams = relationship("Steam", back_populates="user")
    tracking_items = relationship("ItemTrack", back_populates="user")
    tracking_games = relationship("GameTrack", back_populates="user")


# Steam
class Steam(Base):
    steam_id = Column(BigInteger, nullable=False)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.telegram_id"))

    user = relationship("User", back_populates="steams")
    games = relationship("GameInAccount", back_populates="steam", passive_deletes=True)
    inventorys = relationship("Inventory", back_populates="steam", passive_deletes=True)


class Game(Base):
    name = Column(String, nullable=False)
    game_id = Column(Integer, nullable=False, unique=True)
    cost = Column(Integer, nullable=False)

    games_in = relationship(
        "GameInAccount", back_populates="game", passive_deletes=True
    )


class GameInAccount(Base):
    game_name = Column(String, nullable=False)
    first_cost = Column(Integer, nullable=False)
    time_in_game = Column(Integer, nullable=False)
    steam_id = Column(BigInteger, ForeignKey("steams.id", ondelete="CASCADE"))
    game_id = Column(Integer, ForeignKey("games.game_id", ondelete="CASCADE"))

    steam = relationship("Steam", back_populates="games")
    game = relationship(
        "Game",
        back_populates="games_in",
        uselist=False,
    )


class Inventory(Base):
    games_id = Column(Integer, nullable=False)
    steam_id = Column(BigInteger, ForeignKey("steams.id", ondelete="CASCADE"))

    steam = relationship("Steam", back_populates="inventorys")
    items_in = relationship(
        "ItemInInventory", back_populates="inventorys", passive_deletes=True
    )


class ItemInInventory(Base):
    amount = Column(Integer, nullable=False)
    first_cost = Column(Integer, nullable=False)
    inventory_id = Column(Integer, ForeignKey("inventorys.id", ondelete="CASCADE"))
    item_id = Column(BigInteger, ForeignKey("items.classid", ondelete="CASCADE"))

    inventorys = relationship("Inventory", back_populates="items_in")
    item = relationship(
        "Item",
        back_populates="items_in",
        uselist=False,
    )


class Item(Base):
    name = Column(String, nullable=False)
    app_id = Column(Integer, default=730, nullable=False)
    classid = Column(BigInteger, nullable=False, unique=True)
    cost = Column(Integer, nullable=False)

    items_in = relationship(
        "ItemInInventory", back_populates="item", passive_deletes=True
    )


class ItemTrack(Base):
    name = Column(String, nullable=False)
    first_cost = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.telegram_id", ondelete="CASCADE"))
    item_id = Column(BigInteger, ForeignKey("items.classid", ondelete="CASCADE"))

    user = relationship("User", back_populates="tracking_items")


class GameTrack(Base):
    name = Column(String, nullable=False)
    first_cost = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.telegram_id", ondelete="CASCADE"))
    game_id = Column(Integer, ForeignKey("games.game_id", ondelete="CASCADE"))

    user = relationship("User", back_populates="tracking_games")
