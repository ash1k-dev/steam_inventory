from aiogram.filters.callback_data import CallbackData
from typing import Optional


class ItemsCallbackFactory(CallbackData, prefix="items"):
    action: Optional[str] = None
    steam_name: Optional[str] = None
    steam_id: Optional[int] = None
    page: Optional[int] = None
    pages_amount: Optional[int] = None


class GamesCallbackFactory(CallbackData, prefix="games"):
    action: Optional[str] = None
    steam_name: Optional[str] = None
    steam_id: Optional[int] = None
    limit: Optional[int] = None
    order: Optional[str] = None
    page: Optional[int] = None
    pages_amount: Optional[int] = None


class SteamidCallbackFactory(CallbackData, prefix="steamid"):
    action: Optional[str] = None
    steam_name: Optional[str] = None
    steam_id: Optional[int] = None


class GamesTrackCallbackFactory(CallbackData, prefix="games_track"):
    action: Optional[str] = None
    name: Optional[str] = None
    tracking_game_id: Optional[int] = None
    user_id: Optional[int] = None
    first_game_cost: Optional[int] = None
    game_cost: Optional[int] = None
    game_id: Optional[int] = None


class ItemsTrackCallbackFactory(CallbackData, prefix="items_track"):
    action: Optional[str] = None
    name: Optional[str] = None
    tracking_item_id: Optional[int] = None
    user_id: Optional[int] = None
    first_item_cost: Optional[int] = None
    item_cost: Optional[int] = None
    item_id: Optional[int] = None
