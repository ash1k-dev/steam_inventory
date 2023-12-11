from urllib.parse import quote

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from config import ITEMS_ON_PAGE
from redis_data_convert import redis_convert_to_dict
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot.keyboards.inline.callback_factory import ItemsCallbackFactory
from core.bot.keyboards.inline.inline import (
    get_items_back_menu,
    get_items_menu,
    get_pagination,
)
from core.db.methods.request import (
    get_amount_and_items_info_from_db,
    get_items_info_from_db,
)

router = Router()


@router.callback_query(ItemsCallbackFactory.filter())
async def get_items(
    callback: CallbackQuery,
    callback_data: ItemsCallbackFactory,
    session: AsyncSession,
):
    steam_id = callback_data.steam_id
    steam_name = callback_data.steam_name
    user_data = redis_convert_to_dict(f"{callback.from_user.id}")
    if callback_data.action == "info" or callback_data.action == "back":
        (
            difference_total_cost,
            first_total_cost,
            max_cost,
            min_cost,
            total_amount,
            total_cost,
        ) = await get_items_info(session, steam_id, user_data)
        await callback.message.answer(
            text=f"{markdown.hbold('Аккаунт ' + steam_name)}\n"
            f"Количество предметов: {total_amount}\n"
            f"Общая стоимость предметов: {total_cost}руб.\n"
            f"Первоначальная стоимость предметов: {first_total_cost}руб.\n"
            f"Прирост стоимости: {difference_total_cost}руб."
            f"({int((difference_total_cost/first_total_cost)*100)}%)\n"
            f"Максимальная стоимость предмета: {max_cost} \n"
            f"Минимальная стоимость предмета: {min_cost}",
            reply_markup=get_items_menu(
                steam_id=callback_data.steam_id,
                steam_name=callback_data.steam_name,
            ),
        )
    else:
        if callback_data.action == "all":
            all_items = await get_items_list(
                callback_data, session, steam_id, user_data, order="cost"
            )
        elif callback_data.action == "top_cost":
            all_items = await get_items_list(
                callback_data, session, steam_id, user_data, order="cost"
            )
        elif callback_data.action == "top_gain":
            all_items = await get_items_list(
                callback_data,
                session,
                steam_id,
                user_data,
                order="difference",
            )
        grouped_items_list, items_list = await get_items_text(all_items)
        for i in range(0, len(items_list), ITEMS_ON_PAGE):
            grouped_items_list.append("".join(items_list[i : i + ITEMS_ON_PAGE]))
        if len(items_list) <= ITEMS_ON_PAGE:
            await callback.message.answer(
                text=f"{''.join(items_list)}",
                disable_web_page_preview=True,
                reply_markup=get_items_back_menu(
                    steam_id=callback_data.steam_id, steam_name=callback_data.steam_name
                ),
            )
        else:
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
    await callback.answer()


async def get_items_text(all_items):
    items_list = []
    grouped_items_list = []
    for name, item_cost, first_cost, amount, diff in all_items:
        if first_cost != 0:
            items_list.append(
                f"{markdown.hbold(name)}\n"
                f"Текущая стоимость: {item_cost}руб.\n"
                f"Первоначальная стоимость: {first_cost}руб.\n"
                f"Прирост стоимости: {diff}руб.({int(diff / first_cost * 100)}%)\n"
                f"Количество предметов: {amount}\n"
                f"Ссылка на торговую площадку:"
                f" {markdown.hlink('SteamLink', f'https://steamcommunity.com/market/listings/730/{quote(name)}')}\n\n"
            )
    return grouped_items_list, items_list


async def get_items_list(callback_data, session, steam_id, user_data, order):
    if user_data:
        all_items = []
        items = user_data["steam_ids"][f"{steam_id}"]["items"]
        items = [items_data for items_data in items.values()]
        items = sorted(items, key=lambda x: x[order], reverse=True)
        for item in items[: callback_data.limit]:
            name = item["name"]
            cost = item["cost"]
            first_cost = item["first_cost"]
            amount = item["amount"]
            difference = item["difference"]
            all_items.append((name, cost, first_cost, amount, difference))
    else:
        all_items = await get_amount_and_items_info_from_db(
            steam_id=callback_data.steam_id,
            limit=callback_data.limit,
            order=order,
            session=session,
        )
    return all_items


async def get_items_info(session, steam_id, user_data):
    if user_data:
        items_info = user_data["steam_ids"][f"{steam_id}"]["items_info"]
        total_cost = items_info["total_cost"]
        first_total_cost = items_info["first_total_cost"]
        total_amount = items_info["total_amount"]
        max_cost = items_info["max_cost"]
        min_cost = items_info["min_cost"]
        difference_total_cost = total_cost - first_total_cost
    else:
        general_items_info = await get_items_info_from_db(
            steam_id=steam_id, session=session
        )
        (
            total_cost,
            first_total_cost,
            total_amount,
            max_cost,
            min_cost,
        ) = general_items_info[0]
        difference_total_cost = total_cost - first_total_cost
    return (
        difference_total_cost,
        first_total_cost,
        max_cost,
        min_cost,
        total_amount,
        total_cost,
    )
