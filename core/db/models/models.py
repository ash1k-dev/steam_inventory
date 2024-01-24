from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, relationship


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True)


class User(Base):
    name: Mapped[str] = Column(String, nullable=True)
    telegram_id: Mapped[int] = Column(Integer, nullable=False, unique=True)

    steams: Mapped["Steam"] = relationship("Steam", back_populates="user")
    tracking_items: Mapped["ItemTrack"] = relationship(
        "ItemTrack", back_populates="user"
    )
    tracking_games: Mapped["GameTrack"] = relationship(
        "GameTrack", back_populates="user"
    )


# Steam
class Steam(Base):
    steam_id: Mapped[int] = Column(BigInteger, nullable=False)
    name: Mapped[str] = Column(String, nullable=False)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.telegram_id"))

    user: Mapped["User"] = relationship("User", back_populates="steams")
    games: Mapped["GameInAccount"] = relationship(
        "GameInAccount", back_populates="steam", passive_deletes=True
    )
    inventorys: Mapped["Inventory"] = relationship(
        "Inventory", back_populates="steam", passive_deletes=True
    )


class Game(Base):
    name: Mapped[str] = Column(String, nullable=False)
    game_id: Mapped[int] = Column(Integer, nullable=False, unique=True)
    cost: Mapped[int] = Column(Integer, nullable=False)

    games_in: Mapped["GameInAccount"] = relationship(
        "GameInAccount", back_populates="game", passive_deletes=True
    )


class GameInAccount(Base):
    game_name: Mapped[str] = Column(String, nullable=False)
    first_cost: Mapped[int] = Column(Integer, nullable=False)
    time_in_game: Mapped[int] = Column(Integer, nullable=False)
    steam_id: Mapped[int] = Column(
        BigInteger, ForeignKey("steams.id", ondelete="CASCADE")
    )
    game_id: Mapped[int] = Column(
        Integer, ForeignKey("games.game_id", ondelete="CASCADE")
    )

    steam: Mapped["Steam"] = relationship("Steam", back_populates="games")
    game: Mapped["Game"] = relationship(
        "Game",
        back_populates="games_in",
        uselist=False,
    )


class Inventory(Base):
    games_id: Mapped[int] = Column(Integer, nullable=False)
    steam_id: Mapped[int] = Column(
        BigInteger, ForeignKey("steams.id", ondelete="CASCADE")
    )

    steam: Mapped["Steam"] = relationship("Steam", back_populates="inventorys")
    items_in: Mapped["ItemInInventory"] = relationship(
        "ItemInInventory", back_populates="inventorys", passive_deletes=True
    )


class ItemInInventory(Base):
    amount: Mapped[int] = Column(Integer, nullable=False)
    first_cost: Mapped[int] = Column(Integer, nullable=False)
    inventory_id: Mapped[int] = Column(
        Integer, ForeignKey("inventorys.id", ondelete="CASCADE")
    )
    item_id: Mapped[int] = Column(
        BigInteger, ForeignKey("items.classid", ondelete="CASCADE")
    )

    inventorys: Mapped["Inventory"] = relationship(
        "Inventory", back_populates="items_in"
    )
    item: Mapped["Item"] = relationship(
        "Item",
        back_populates="items_in",
        uselist=False,
    )


class Item(Base):
    name: Mapped[str] = Column(String, nullable=False)
    app_id: Mapped[int] = Column(Integer, default=730, nullable=False)
    classid: Mapped[int] = Column(BigInteger, nullable=False, unique=True)
    cost = Column(Integer, nullable=False)

    items_in: Mapped["ItemInInventory"] = relationship(
        "ItemInInventory", back_populates="item", passive_deletes=True
    )


class ItemTrack(Base):
    name: Mapped[str] = Column(String, nullable=False)
    first_cost: Mapped[int] = Column(Integer, nullable=False)
    user_id: Mapped[int] = Column(
        Integer, ForeignKey("users.telegram_id", ondelete="CASCADE")
    )
    item_id: Mapped[int] = Column(
        BigInteger, ForeignKey("items.classid", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship("User", back_populates="tracking_items")


class GameTrack(Base):
    name: Mapped[str] = Column(String, nullable=False)
    first_cost: Mapped[int] = Column(Integer, nullable=False)
    user_id: Mapped[int] = Column(
        Integer, ForeignKey("users.telegram_id", ondelete="CASCADE")
    )
    game_id: Mapped[int] = Column(
        Integer, ForeignKey("games.game_id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship("User", back_populates="tracking_games")
