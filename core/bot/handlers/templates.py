from string import Template


TEXT_ITEMS = Template(
    "<b>${item_name}</b>\n"
    "Текущая стоимость: ${item_cost}руб.\n"
    "Первоначальная стоимость: ${first_item_cost}руб.\n"
    "Прирост стоимости: ${difference}руб.(${difference_percents}%)\n"
    "Количество предметов: ${amount}\n"
    "Ссылка на торговую площадку: ${link}\n\n"
)

TEXT_ITEMS_INFO = Template(
    "<b>Аккаунт ${steam_name}</b>\n"
    "Количество предметов: ${total_amount}\n"
    "Общая стоимость предметов: ${total_cost}руб.\n"
    "Первоначальная стоимость предметов: ${first_total_cost}руб.\n"
    "Прирост стоимости: ${difference_total_cost}руб. (${difference_percents}%)\n"
    "Максимальная стоимость предмета: ${max_cost}\n"
    "Минимальная стоимость предмета: ${min_cost}\n"
)

TEXT_GAMES = Template(
    "<b>${game_name}</b>\n"
    "Количество часов: ${time_in_game}\n"
    "Актуальная стоимость: ${game_cost}\n"
    "Первоначальная стоимость: ${first_game_cost}\n"
    "Ссылка на торговую площадку: ${link}\n\n"
)

TEXT_GAMES_INFO = Template(
    "<b>Аккаунт ${steam_name}</b>\n"
    "Количество: ${number_of_games}\n"
    "Общая стоимость: ${total_cost}\n"
    "Общее количество часов: ${time_in_games}",
)


TEXT_ADD_STEAM_PROCESS = Template(
    "Происходит добавление steam id <b>${steam_id}</b>"
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
