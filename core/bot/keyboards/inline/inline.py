from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from core.bot.keyboards.inline.callback_factory import (
    SteamidCallbackFactory,
    ItemsCallbackFactory,
    GamesCallbackFactory,
    GamesTrackCallbackFactory,
    ItemsTrackCallbackFactory,
)


def get_steams_menu(steam_id_list: list) -> InlineKeyboardMarkup:
    """Keyboard to steams menu"""
    keyboard_builder = InlineKeyboardBuilder()
    for steam_id in steam_id_list:
        keyboard_builder.button(
            text=steam_id.name,
            callback_data=SteamidCallbackFactory(
                action="steamid",
                steam_name=steam_id.name,
                steam_id=steam_id.steam_id,
            ),
        )
    keyboard_builder.button(
        text="Добавить 🪄", callback_data=SteamidCallbackFactory(action="add_steam_id")
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_control_menu(steamid_name: str, steamid_id) -> InlineKeyboardMarkup:
    """Keyboard to delete a steam id"""
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
    """Keyboard to games menu"""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="ТОП 5 по проведенному времени",
        callback_data=GamesCallbackFactory(
            action="time",
            steam_name=steam_name,
            steam_id=steam_id,
            limit=5,
            order="time",
        ),
    )
    keyboard_builder.button(
        text="ТОП 5 по стоимости",
        callback_data=GamesCallbackFactory(
            action="cost",
            steam_name=steam_name,
            steam_id=steam_id,
            limit=5,
            order="cost",
        ),
    )
    keyboard_builder.button(
        text="Все игры",
        callback_data=GamesCallbackFactory(
            action="all",
            steam_name=steam_name,
            steam_id=steam_id,
            limit=10000,
            order="all",
            page=0,
            pages_amount=5,
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
    """Keyboard to games menu"""
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
    """Keyboard to items menu"""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="ТОП 5 предметов по стоимости",
        callback_data=ItemsCallbackFactory(
            action="top_cost",
            steam_name=steam_name,
            steam_id=steam_id,
            page=0,
            pages_amount=5,
        ),
    )
    keyboard_builder.button(
        text="ТОП 5 предметов по приросту стоимости",
        callback_data=ItemsCallbackFactory(
            action="top_gain",
            steam_name=steam_name,
            steam_id=steam_id,
            page=0,
            pages_amount=5,
        ),
    )
    keyboard_builder.button(
        text="Все предметы",
        callback_data=ItemsCallbackFactory(
            action="all",
            steam_name=steam_name,
            steam_id=steam_id,
            page=0,
            pages_amount=10,
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
    pages_amount,
    action,
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
                action=action,
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
                action=action,
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
                action=action,
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
                action=action,
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
    """Keyboard to games menu"""
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
    """Keyboard to steams menu"""
    keyboard_builder = InlineKeyboardBuilder()
    for user_id, name, game_id, first_game_cost, game_cost in tracking_games_list:
        keyboard_builder.button(
            text=name,
            callback_data=GamesTrackCallbackFactory(
                action="tracking_game",
                # tracking_game_id=game_id,
                # name=name,
                # first_game_cost=first_game_cost,
                # game_cost=game_cost,
                # user_id=user_id,
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
    """Keyboard to steams menu"""
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


def get_control_menu_tracking_game(game_id: int, game_name) -> InlineKeyboardMarkup:
    """Keyboard to delete a steam id"""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Удалить",
        callback_data=GamesTrackCallbackFactory(
            action="delete",
            name=game_name,
            game_id=game_id,
        ),
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_confirm_tracking_item_menu(item_id) -> InlineKeyboardMarkup:
    """Keyboard to steams menu"""
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


def get_control_menu_tracking_items(item_id: int, item_name) -> InlineKeyboardMarkup:
    """Keyboard to delete a steam id"""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Удалить",
        callback_data=ItemsTrackCallbackFactory(
            action="delete",
            # name=item_name,
            item_id=item_id,
        ),
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_tracking_items_menu(tracking_items_list: list) -> InlineKeyboardMarkup:
    """Keyboard to steams menu"""
    keyboard_builder = InlineKeyboardBuilder()
    for name, first_item_cost, user_id, item_id, item_cost in tracking_items_list:
        keyboard_builder.button(
            text=name,
            callback_data=ItemsTrackCallbackFactory(
                action="tracking_item",
                # name=name,
                # first_item_cost=first_item_cost,
                # user_id=user_id,
                item_id=item_id,
                # item_cost=item_cost,
            ),
        )
    keyboard_builder.button(
        text="Добавить 🪄",
        callback_data=ItemsTrackCallbackFactory(action="add_tracking_item"),
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
