from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from config import ITEMS_LIMIT, TOP_ITEMS_AMOUNT
from core.bot.keyboards.inline.callback_factory import (
    GamesCallbackFactory,
    GamesTrackCallbackFactory,
    ItemsCallbackFactory,
    ItemsTrackCallbackFactory,
    SteamidCallbackFactory,
)


def get_steams_menu(steam_id_list: list) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    for steam_id, name in steam_id_list:
        keyboard_builder.button(
            text=name,
            callback_data=SteamidCallbackFactory(
                action="steamid",
                steam_name=name,
                steam_id=steam_id,
            ),
        )
    keyboard_builder.button(
        text="Добавить 🪄", callback_data=SteamidCallbackFactory(action="add_steam_id")
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_control_menu(steamid_name: str, steamid_id) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Информация",
        callback_data=SteamidCallbackFactory(
            action="info",
            steam_name=steamid_name,
            steam_id=steamid_id,
        ),
    )
    keyboard_builder.button(
        text="Удалить",
        callback_data=SteamidCallbackFactory(
            action="delete",
            steam_name=steamid_name,
            steam_id=steamid_id,
        ),
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_steam_id_menu(steamid_name, steamid_id) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Инвентарь",
        callback_data=ItemsCallbackFactory(
            action="info",
            steam_name=steamid_name,
            steam_id=steamid_id,
        ),
    )
    keyboard_builder.button(
        text="Игры",
        callback_data=GamesCallbackFactory(
            action="info",
            steam_name=steamid_name,
            steam_id=steamid_id,
        ),
    )
    keyboard_builder.button(
        text="Назад",
        callback_data=SteamidCallbackFactory(
            action="steamid",
            steam_name=steamid_name,
            steam_id=steamid_id,
        ),
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_games_menu(steam_id, steam_name) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text=f"ТОП {TOP_ITEMS_AMOUNT} по проведенному времени",
        callback_data=GamesCallbackFactory(
            action="time",
            steam_name=steam_name,
            steam_id=steam_id,
            page=0,
            order="time",
            limit=TOP_ITEMS_AMOUNT,
        ),
    )
    keyboard_builder.button(
        text=f"ТОП {TOP_ITEMS_AMOUNT} по стоимости",
        callback_data=GamesCallbackFactory(
            action="cost",
            steam_name=steam_name,
            steam_id=steam_id,
            page=0,
            order="cost",
            limit=TOP_ITEMS_AMOUNT,
        ),
    )
    keyboard_builder.button(
        text="Все игры",
        callback_data=GamesCallbackFactory(
            action="all",
            steam_name=steam_name,
            steam_id=steam_id,
            page=0,
            order="time",
            limit=ITEMS_LIMIT,
        ),
    )
    keyboard_builder.button(
        text="Назад",
        callback_data=SteamidCallbackFactory(
            action="info", steam_name=steam_name, steam_id=steam_id
        ),
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_games_back_menu(steam_id, steam_name) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Назад",
        callback_data=GamesCallbackFactory(
            action="info",
            steam_name=steam_name,
            steam_id=steam_id,
        ),
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_items_menu(steam_id: int, steam_name: str) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text=f"ТОП {TOP_ITEMS_AMOUNT} предметов по стоимости",
        callback_data=ItemsCallbackFactory(
            # action="cost",
            steam_name=steam_name,
            steam_id=steam_id,
            page=0,
            order="cost",
            limit=TOP_ITEMS_AMOUNT,
        ),
    )
    keyboard_builder.button(
        text=f"ТОП {TOP_ITEMS_AMOUNT} предметов по приросту стоимости",
        callback_data=ItemsCallbackFactory(
            # action="gain",
            steam_name=steam_name,
            steam_id=steam_id,
            page=0,
            order="difference",
            limit=TOP_ITEMS_AMOUNT,
        ),
    )
    keyboard_builder.button(
        text="Все предметы",
        callback_data=ItemsCallbackFactory(
            action="all",
            steam_name=steam_name,
            steam_id=steam_id,
            page=0,
            order="cost",
            limit=ITEMS_LIMIT,
        ),
    )
    keyboard_builder.button(
        text="Назад",
        callback_data=SteamidCallbackFactory(
            action="info", steam_name=steam_name, steam_id=steam_id
        ),
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_pagination(
    page,
    steam_name,
    steam_id,
    # action,
    pages_amount,
    callbackfactory,
    limit=None,
    order=None,
) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    if page == 0:
        keyboard_builder.button(text=f"{page+1}/{pages_amount}", callback_data="null")
        keyboard_builder.button(
            text="Next",
            callback_data=callbackfactory(
                # action=action,
                steam_name=steam_name,
                steam_id=steam_id,
                page=page + 1,
                pages_amount=pages_amount,
                limit=limit,
                order=order,
            ),
        )
        keyboard_builder.button(
            text="Назад",
            callback_data=callbackfactory(
                action="back",
                steam_name=steam_name,
                steam_id=steam_id,
            ),
        )
        keyboard_builder.adjust(2, 1, repeat=True)
    if page == pages_amount - 1:
        keyboard_builder.button(
            text="Previous",
            callback_data=callbackfactory(
                # action=action,
                steam_name=steam_name,
                steam_id=steam_id,
                page=page - 1,
                pages_amount=pages_amount,
                limit=limit,
                order=order,
            ),
        )
        keyboard_builder.button(text=f"{page+1}/{pages_amount}", callback_data="null")
        keyboard_builder.button(
            text="Назад",
            callback_data=callbackfactory(
                action="back",
                steam_name=steam_name,
                steam_id=steam_id,
            ),
        )
        keyboard_builder.adjust(2, 1, repeat=True)
    elif page > 0:
        keyboard_builder.button(
            text="Previous",
            callback_data=callbackfactory(
                # action=action,
                steam_name=steam_name,
                steam_id=steam_id,
                page=page - 1,
                pages_amount=pages_amount,
                limit=limit,
                order=order,
            ),
        )
        keyboard_builder.button(text=f"{page+1}/{pages_amount}", callback_data="null")
        keyboard_builder.button(
            text="Next",
            callback_data=callbackfactory(
                # action=action,
                steam_name=steam_name,
                steam_id=steam_id,
                page=page + 1,
                pages_amount=pages_amount,
                limit=limit,
                order=order,
            ),
        )
        keyboard_builder.button(
            text="Назад",
            callback_data=callbackfactory(
                action="back",
                steam_name=steam_name,
                steam_id=steam_id,
            ),
        )
        keyboard_builder.adjust(3, 1, repeat=True)
    return keyboard_builder.as_markup()


def get_items_back_menu(steam_id, steam_name) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Назад",
        callback_data=ItemsCallbackFactory(
            action="info",
            steam_name=steam_name,
            steam_id=steam_id,
        ),
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_tracking_games_menu(tracking_games_list: list) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    for name, game_id, first_game_cost, game_cost in tracking_games_list:
        keyboard_builder.button(
            text=name,
            callback_data=GamesTrackCallbackFactory(
                action="tracking_game",
                game_id=game_id,
            ),
        )
    keyboard_builder.button(
        text="Добавить 🪄",
        callback_data=GamesTrackCallbackFactory(action="add_tracking_game"),
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_confirm_tracking_game_menu(game_id) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Да",
        callback_data=GamesTrackCallbackFactory(
            action="add_tracking_game_confirm", game_id=game_id
        ),
    )
    keyboard_builder.button(
        text="Нет",
        callback_data=GamesTrackCallbackFactory(action="add_tracking_game_not_confirm"),
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_control_menu_tracking_game(game_id: int) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Удалить",
        callback_data=GamesTrackCallbackFactory(
            action="delete",
            game_id=game_id,
        ),
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_confirm_tracking_item_menu(item_id) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Да",
        callback_data=ItemsTrackCallbackFactory(
            action="add_tracking_item_confirm", item_id=item_id
        ),
    )
    keyboard_builder.button(
        text="Нет",
        callback_data=ItemsTrackCallbackFactory(action="add_tracking_item_not_confirm"),
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_control_menu_tracking_items(item_id: int) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Удалить",
        callback_data=ItemsTrackCallbackFactory(
            action="delete",
            item_id=item_id,
        ),
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_tracking_items_menu(tracking_items_list: list) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    for name, item_id, first_item_cost, item_cost in tracking_items_list:
        keyboard_builder.button(
            text=name,
            callback_data=ItemsTrackCallbackFactory(
                action="tracking_item",
                item_id=item_id,
            ),
        )
    keyboard_builder.button(
        text="Добавить 🪄",
        callback_data=ItemsTrackCallbackFactory(action="add_tracking_item"),
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
