from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


def get_main_menu() -> ReplyKeyboardMarkup:
    """Main keyboard"""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Мои Steam id")
    keyboard_builder.button(text="Отслеживание стоимости")
    keyboard_builder.button(text="Помощь")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)



def get_items_and_games_menu() -> ReplyKeyboardMarkup:
    """Items and games keyboard"""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Предметы")
    keyboard_builder.button(text="Игры")
    keyboard_builder.button(text="Назад")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_items_menu() -> ReplyKeyboardMarkup:
    """Items keyboard"""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Текущая стоимость скинов")
    keyboard_builder.button(text="Динамика изменения")
    keyboard_builder.button(text="Назад")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_games_menu() -> ReplyKeyboardMarkup:
    """Games keyboard"""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Текущая стоимость игр")
    keyboard_builder.button(text="Время в играх")
    keyboard_builder.button(text="Назад")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)



def get_check_cost_menu() -> ReplyKeyboardMarkup:
    """Сheck cost keyboard"""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Предметы")
    keyboard_builder.button(text="Игры")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)