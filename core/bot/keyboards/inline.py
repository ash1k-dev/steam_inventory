from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def get_steams_menu(steam_id_list: list) -> InlineKeyboardMarkup:
    """Keyboard to steams menu"""
    keyboard_builder = InlineKeyboardBuilder()
    for steam_id in steam_id_list:
        keyboard_builder.button(
            text=steam_id.steam_name,
            callback_data=f"steamid_{steam_id.steam_name}_{steam_id.steam_id}",
        )
    keyboard_builder.button(text="Добавить 🪄", callback_data="add_steam_id")
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
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_steam_id_menu(steamid_name, steamid_id) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Инвентарь", callback_data=f"inventory_{steamid_name}_{steamid_id}"
    )
    keyboard_builder.button(
        text="Игры", callback_data=f"games_info_{steamid_name}_{steamid_id}"
    )
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


def get_items_menu(steam_id: int) -> InlineKeyboardMarkup:
    """Keyboard to items menu"""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="ТОП 5 предметов по приросту стоимости",
        callback_data=f"items_list_top_{steam_id}",
    )
    keyboard_builder.button(
        text="Все предметы", callback_data=f"items_list_all_{steam_id}"
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
