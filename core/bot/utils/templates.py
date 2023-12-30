from string import Template

TEXT_CHANGING = Template(
    "<b>${name}</b>\n"
    "Первоначальная стоимость: ${first_cost} \n"
    "Актуальная стоимость: ${cost} \n"
    "Изменение: ${difference} руб.(${difference_percents}%)\n"
    "Ссылка: ${link}\n\n"
)
