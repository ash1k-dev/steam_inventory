from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


def get_main_menu() -> ReplyKeyboardMarkup:
    """Создание главного меню"""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Мои Steam id")
    keyboard_builder.button(text="Отслеживание стоимости")
    keyboard_builder.button(text="Помощь")
    keyboard_builder.adjust(2, 1)
    return keyboard_builder.as_markup(resize_keyboard=True)


def get_track_menu() -> ReplyKeyboardMarkup:
    """Создание меню отслеживания стоимости предметов и игр"""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Предметы")
    keyboard_builder.button(text="Игры")
    keyboard_builder.button(text="Назад")
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(resize_keyboard=True)
