from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from typing import Optional
from aiogram.filters.callback_data import CallbackData


class ItemsCallbackFactory(CallbackData, prefix="items"):
    action: Optional[str] = None
    steam_name: Optional[str] = None
    steam_id: Optional[int] = None
    page: Optional[int] = None
    pages_amount: Optional[int] = None


def get_steams_menu(steam_id_list: list) -> InlineKeyboardMarkup:
    """Keyboard to steams menu"""
    keyboard_builder = InlineKeyboardBuilder()
    for steam_id in steam_id_list:
        keyboard_builder.button(
            text=steam_id.steam_name,
            callback_data=f"steamid_{steam_id.steam_name}_{steam_id.steam_id}",
        )
    keyboard_builder.button(text="Добавить 🪄", callback_data="add_steam_id")
    # keyboard_builder.button(text="Добавить 🪄", callback_data="add")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_control_menu(steamid_name: str, steamid_id) -> InlineKeyboardMarkup:
    """Keyboard to delete a steam id"""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Информация", callback_data=f"info_{steamid_name}_{steamid_id}"
    )
    keyboard_builder.button(
        text="Удалить", callback_data=f"delete_{steamid_name}_{steamid_id}"
    )
    keyboard_builder.button(text="Назад", callback_data="back")
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
        text="Игры", callback_data=f"games_info_{steamid_name}_{steamid_id}"
    )
    keyboard_builder.button(
        text="Назад", callback_data=f"steamid_{steamid_name}_{steamid_id}"
    )
    # keyboard_builder.button(text="Тест", callback_data=f"page_start_0")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_games_menu() -> InlineKeyboardMarkup:
    """Keyboard to games menu"""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="ТОП 5 по проведенному времени", callback_data=f"games_list_time"
    )
    keyboard_builder.button(text="ТОП 5 по стоимости", callback_data=f"games_list_cost")
    keyboard_builder.button(text="Все игры", callback_data=f"games_list_all")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_items_menu(steam_id: int, steam_name: str) -> InlineKeyboardMarkup:
    """Keyboard to items menu"""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="ТОП 5 предметов по приросту стоимости",
        callback_data=ItemsCallbackFactory(
            action="top",
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
    keyboard_builder.button(text="Назад", callback_data=f"info_{steam_name}_{steam_id}")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_pagination(
    page, steam_name, steam_id, pages_amount, action
) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    if page == 0:
        keyboard_builder.button(text=f"{page+1}/{pages_amount}", callback_data="null")
        keyboard_builder.button(
            text="Next",
            callback_data=ItemsCallbackFactory(
                action=action,
                steam_name=steam_name,
                steam_id=steam_id,
                page=page + 1,
                pages_amount=pages_amount,
            ),
        )
        keyboard_builder.button(
            text="Назад",
            callback_data=ItemsCallbackFactory(
                action="back",
                steam_name=steam_name,
                steam_id=steam_id,
            ),
        )
        keyboard_builder.adjust(2, 1, repeat=True)
    if page == pages_amount - 1:
        keyboard_builder.button(
            text="Previous",
            callback_data=ItemsCallbackFactory(
                action=action,
                steam_name=steam_name,
                steam_id=steam_id,
                page=page - 1,
                pages_amount=pages_amount,
            ),
        )
        keyboard_builder.button(text=f"{page+1}/{pages_amount}", callback_data="null")
        keyboard_builder.button(
            text="Назад",
            callback_data=ItemsCallbackFactory(
                action="back",
                steam_name=steam_name,
                steam_id=steam_id,
            ),
        )
        keyboard_builder.adjust(2, 1, repeat=True)
    elif page > 0:
        keyboard_builder.button(
            text="Previous",
            callback_data=ItemsCallbackFactory(
                action=action,
                steam_name=steam_name,
                steam_id=steam_id,
                page=page - 1,
                pages_amount=pages_amount,
            ),
        )
        keyboard_builder.button(text=f"{page+1}/{pages_amount}", callback_data="null")
        keyboard_builder.button(
            text="Next",
            callback_data=ItemsCallbackFactory(
                action=action,
                steam_name=steam_name,
                steam_id=steam_id,
                page=page + 1,
                pages_amount=pages_amount,
            ),
        )
        keyboard_builder.button(
            text="Назад",
            callback_data=ItemsCallbackFactory(
                action="back",
                steam_name=steam_name,
                steam_id=steam_id,
            ),
        )
        keyboard_builder.adjust(3, 1, repeat=True)
    return keyboard_builder.as_markup()
