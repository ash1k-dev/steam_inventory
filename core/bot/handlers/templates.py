from string import Template

TEXT_ITEM = Template(
    "<b>${item_name}</b>\n"
    "Текущая стоимость: ${item_cost}руб.\n"
    "Первоначальная стоимость: ${first_item_cost}руб.\n"
    "Прирост стоимости: ${difference}руб.(${difference_percents}%)\n"
    "Количество предметов: ${amount}\n"
    "Ссылка на торговую площадку: ${link}\n\n"
)

TEXT_ITEMS_INFO = Template(
    "<b>Предметы ${steam_name}</b>\n"
    "Количество: ${total_amount}\n"
    "Общая стоимость: ${total_cost}руб.\n"
    "Первоначальная стоимость: ${first_total_cost}руб.\n"
    "Прирост стоимости: ${difference_total_cost}руб. (${difference_percents}%)\n"
    "Максимальная стоимость: ${max_cost}\n"
    "Минимальная стоимость: ${min_cost}\n"
)

TEXT_GAME = Template(
    "<b>${game_name}</b>\n"
    "Количество часов: ${time_in_game}\n"
    "Актуальная стоимость: ${game_cost}\n"
    "Первоначальная стоимость: ${first_game_cost}\n"
    "Ссылка на торговую площадку: ${link}\n\n"
)

TEXT_GAMES_INFO = Template(
    "<b>Игры ${steam_name}</b>\n"
    "Количество: ${number_of_games}\n"
    "Общая стоимость: ${total_cost}\n"
    "Общее количество часов: ${time_in_games}",
)


TEXT_ADD_STEAM_PROCESS = Template(
    "Происходит добавление Steam id <b>${steam_id}</b>"
    " с именем <b>'${steam_name}'</b>.\n"
    "Обработка данных займет какое-то время и зависит"
    " от количества предметов и игр на Вашем аккаунте"
)

TEXT_ADD_STEAM_FINAL = Template(
    "Для Steam id <b>'${steam_id}'</b> с именем <b>'${steam_name}'</b> данные добавлены"
)

TEXT_STEAM_DELETE = Template(
    "Steam id <b>${steam_id}</b> c именем <b>'${steam_name}'</b> успешно удален"
)

TEXT_STEAM_INFO = Template(
    "<b>Имя в профиле:</b> ${steam_name} \n" "<b>Steam id:</b> ${steam_id}"
)


TEXT_ADD_STEAM_ERROR = Template(
    "При добавлении Steam id - ${steam_id} произошла ошибка,"
    " попробуйте повторить через ${repeat_time}"
)


TEXT_ADD_STEAM_ERROR_REPEAT = Template(
    "Вы пытались ранее добавить этот Steam id, попробуйту позже."
    " До повторной попытки осталось - ${text_minute}"
)

TEXT_TRACKING_GAME_CHECK = Template("Это Ваша игра? \n\n ${link}")

TEXT_TRACKING_ITEM_CHECK = Template("Это Ваш предмет? \n\n ${link}")


TEXT_TRACKING_ITEM = Template(
    "<b>${name}</b>\n"
    "Текущая стоимость: ${cost}руб.\n"
    "Первоначальная стоимость: ${first_cost}руб.\n"
    "Изменение: ${difference}руб.(${difference_percents}%)\n"
    "Ссылка: ${link}\n\n"
)


TEXT_TRACKING_GAME = Template(
    "<b>${name}</b>\n"
    "Текущая стоимость: ${cost}руб.\n"
    "Первоначальная стоимость: ${first_cost}руб.\n"
    "Изменение: ${difference}руб.\n"
    "Ссылка: ${link}\n\n"
)

TEXT_HELP = Template(
    "Добавление аккаунта Steam:\n"
    "1. Добавление возможно по steam id или же по имени (если была замена steam id на имя)\n"
    "2. Скорость добавления зависит от количества предметов и игр на аккаунте "
    "(Steam блокирует отправку большого количества запросов разом)\n\n"
    "Отслеживание игр и предметов:\n"
    "1. В список отслеживаемых невозможно добавить игры не доступные в Вашей стране, "
    "а также игры чья стоимость равна нулю (так как это максимально выгодная стоимость)\n"
    "2. Для добавления предметов используйте classid, его можно узнать на странице с предметом в Steam "
    "(через браузер исследуя страницу)\n\n"
    "При возникновении вопросов пишите ${admin_link}"
)
