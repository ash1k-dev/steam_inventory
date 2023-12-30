from typing import Optional

from aiogram.filters.callback_data import CallbackData


class ItemsCallbackFactory(CallbackData, prefix="items"):
    action: Optional[str] = None
    steam_name: Optional[str] = None
    steam_id: Optional[int] = None
    limit: Optional[int] = None
    order: Optional[str] = None
    page: Optional[int] = None


class GamesCallbackFactory(CallbackData, prefix="games"):
    action: Optional[str] = None
    steam_name: Optional[str] = None
    steam_id: Optional[int] = None
    limit: Optional[int] = None
    order: Optional[str] = None
    page: Optional[int] = None


class SteamidCallbackFactory(CallbackData, prefix="steamid"):
    action: Optional[str] = None
    steam_name: Optional[str] = None
    steam_id: Optional[int] = None


class GamesTrackCallbackFactory(CallbackData, prefix="games_track"):
    action: Optional[str] = None
    game_id: Optional[int] = None


class ItemsTrackCallbackFactory(CallbackData, prefix="items_track"):
    action: Optional[str] = None
    item_id: Optional[int] = None
