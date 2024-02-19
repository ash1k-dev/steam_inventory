from typing import Optional

from aiogram.filters.callback_data import CallbackData


class ItemsCallbackFactory(CallbackData, prefix="items"):
    """Фабрика для inline клавиатуры с предметами."""

    action: Optional[str] = None
    steam_name: Optional[str] = None
    steam_id: Optional[int] = None
    limit: Optional[int] = None
    order: Optional[str] = None
    page: Optional[int] = None


class GamesCallbackFactory(CallbackData, prefix="games"):
    """Фабрика для inline клавиатуры с играми."""

    action: Optional[str] = None
    steam_name: Optional[str] = None
    steam_id: Optional[int] = None
    limit: Optional[int] = None
    order: Optional[str] = None
    page: Optional[int] = None


class SteamidCallbackFactory(CallbackData, prefix="steamid"):
    """Фабрика для inline клавиатуры с Steam id"""

    action: Optional[str] = None
    steam_name: Optional[str] = None
    steam_id: Optional[int] = None


class GamesTrackCallbackFactory(CallbackData, prefix="games_track"):
    """Фабрика для inline клавиатуры с отслеживаемыми играми"""

    action: Optional[str] = None
    game_id: Optional[int] = None


class ItemsTrackCallbackFactory(CallbackData, prefix="items_track"):
    """Фабрика для inline клавиатуры с отслеживаемыми предметами"""

    action: Optional[str] = None
    item_id: Optional[int] = None
