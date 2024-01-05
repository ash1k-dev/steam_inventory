from string import Template

TEXT_CHANGING = Template(
    "<b>${name}</b>\n"
    "Первоначальная стоимость: ${first_cost} \n"
    "Актуальная стоимость: ${cost} \n"
    "Изменение: ${difference} руб.(${difference_percents}%)\n"
    "Ссылка: ${link}\n\n"
)


TEXT_STEAM_DATA_ERROR = Template(
    "Ошибка у пользователя - ${user_name}(telegram id: ${user_id})"
    " при добавлении данных Steam id - ${steam_id}. Текст ошибки: ${error} ",
)
