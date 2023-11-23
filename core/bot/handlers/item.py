from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils import markdown


from urllib.parse import quote


from core.db.methods.request import (
    get_amount_and_items_info_from_db,
    get_items_info_from_db,
)


from core.bot.keyboards.inline import ItemsCallbackFactory, get_items_back_menu

from core.bot.keyboards.inline import (
    get_items_menu,
    get_pagination,
)
from aiogram.fsm.storage.redis import RedisStorage
import json


router = Router()


@router.callback_query(ItemsCallbackFactory.filter())
async def get_items(
    callback: CallbackQuery,
    callback_data: ItemsCallbackFactory,
    session: AsyncSession,
    storage: RedisStorage,
):
    steam_id = callback_data.steam_id
    steam_name = callback_data.steam_name
    general_items_info = await get_items_info_from_db(
        steam_id=steam_id, session=session
    )
    total_cost, first_total_cost, total_amount, max_cost, min_cost = general_items_info[
        0
    ]
    difference_total_cost = total_cost - first_total_cost
    items_dict = []
    items_info = await get_amount_and_items_info_from_db(
        steam_id=steam_id, session=session
    )
    for name, item_cost, first_cost, amount in items_info:
        cost = amount * item_cost
        first_cost = amount * first_cost
        # total_cost += cost
        # first_total_cost += first_cost
        store = f"https://steamcommunity.com/market/listings/730/{quote(name)}"
        diff = item_cost - first_cost
        if first_cost != 0:
            items_dict.append(
                {
                    "name": name,
                    "cost": cost,
                    "first_cost": first_cost,
                    "diff": diff,
                    "diff_percent": int(diff / first_cost * 100),
                    "amount": amount,
                    "store": store,
                }
            )
    if callback_data.action == "all":
        grouped_items_list = get_grouped_items_list(
            items_dict=items_dict, filter="cost"
        )
        await callback.message.edit_text(
            text=f"{grouped_items_list[callback_data.page]}",
            disable_web_page_preview=True,
            reply_markup=get_pagination(
                action="all",
                callbackfactory=ItemsCallbackFactory,
                page=callback_data.page,
                pages_amount=len(grouped_items_list),
                steam_id=callback_data.steam_id,
                steam_name=callback_data.steam_name,
            ),
        )
    elif callback_data.action == "top_cost":
        grouped_items_list = get_grouped_items_list(
            items_dict=items_dict, filter="cost"
        )
        await callback.message.edit_text(
            text=f"{grouped_items_list[callback_data.page]}",
            disable_web_page_preview=True,
            reply_markup=get_items_back_menu(
                steam_id=callback_data.steam_id, steam_name=callback_data.steam_name
            ),
        )
    elif callback_data.action == "top_gain":
        grouped_items_list = get_grouped_items_list(
            items_dict=items_dict, filter="diff_percent"
        )
        await callback.message.edit_text(
            text=f"{grouped_items_list[callback_data.page]}",
            disable_web_page_preview=True,
            reply_markup=get_items_back_menu(
                steam_id=callback_data.steam_id, steam_name=callback_data.steam_name
            ),
        )
    elif callback_data.action == "info" or callback_data.action == "back":
        await callback.message.answer(
            text=f"{markdown.hbold('Аккаунт ' + steam_name)}\n"
            f"Количество предметов: {total_amount}\n"
            f"Общая стоимость предметов: {total_cost}руб.\n"
            f"Первоначальная стоимость предметов: {first_total_cost}руб.\n"
            f"Прирост стоимости: {difference_total_cost}руб.({int((difference_total_cost/first_total_cost)*100)}%)\n"
            f"Максимальная стоимость предмета: {max_cost} \n"
            f"Минимальная стоимость предмета: {min_cost}",
            reply_markup=get_items_menu(
                steam_id=callback_data.steam_id,
                steam_name=callback_data.steam_name,
            ),
        )


def get_grouped_items_list(items_dict: list, filter: str) -> list:
    items_list = []
    grouped_items_list = []
    items_dict = sorted(items_dict, key=lambda x: x[f"{filter}"], reverse=True)
    for item in items_dict:
        items_list.append(
            f"{markdown.hbold(item['name'])}\n"
            f"Текущая стоимость: {item['cost']}руб.\n"
            f"Первоначальная стоимость: {item['first_cost']}руб.\n"
            f"Прирост стоимости: {item['diff']}руб.({item['diff_percent']}%)\n"
            f"Количество предметов: {item['amount']}\n"
            f"Ссылка на торговую площадку: {markdown.hlink('SteamLink', item['store'])}\n\n"
        )
    for i in range(0, len(items_list), 5):
        grouped_items_list.append("".join(items_list[i : i + 5]))
    return grouped_items_list
