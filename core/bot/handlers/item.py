from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from urllib.parse import quote


from core.db.methods.request import (
    get_amount_and_items_info_from_db,
)


from core.bot.keyboards.inline import ItemsCallbackFactory


from core.bot.keyboards.inline import (
    get_items_menu,
    get_pagination,
)

router = Router()


@router.callback_query(ItemsCallbackFactory.filter())
async def test_change(
    callback: CallbackQuery, callback_data: ItemsCallbackFactory, session: AsyncSession
):
    steam_id = callback_data.steam_id
    steam_name = callback_data.steam_name
    items_info = await get_amount_and_items_info_from_db(
        steam_id=steam_id, session=session
    )
    total_cost = 0
    first_total_cost = 0
    amount = 0
    max_cost = 0
    min_cost = 10000000
    all_items_list = []
    for k, item in enumerate(items_info):
        name = item.steam_item.name
        cost = item.amount * item.steam_item.item_cost
        first_cost = item.amount * item.steam_item.first_item_cost
        total_cost += cost
        first_total_cost += first_cost
        store = f"https://steamcommunity.com/market/listings/730/{quote(item.steam_item.name)}"
        amount += 1
        if item.steam_item.item_cost > max_cost:
            max_cost = item.steam_item.item_cost
        if 0 < item.steam_item.item_cost < min_cost:
            min_cost = item.steam_item.item_cost
        diff = item.steam_item.item_cost - item.steam_item.first_item_cost
        if first_cost != 0:
            all_items_list.append(
                f"{name}\n"
                f"Первоначальная стоимость: {first_cost}руб.\n"
                f"Текущая стоимость предмета: {cost}руб.\n"
                f"Прирост стоимости: {diff}руб.({int(diff/first_cost*100)}%)\n"
                f"Ссылка на торговую площадку: {store}\n\n"
            )
    difference_total_cost = total_cost - first_total_cost
    if callback_data.action == "all":
        await callback.message.edit_text(
            text=f"{all_items_list[callback_data.page]}",
            disable_webpage_preview=True,
            reply_markup=get_pagination(
                action="all",
                page=callback_data.page,
                pages_amount=callback_data.pages_amount,
                steam_id=callback_data.steam_id,
                steam_name=callback_data.steam_name,
            ),
        )
    elif callback_data.action == "top":
        await callback.message.edit_text(
            text=f"{all_items_list[callback_data.page]}",
            disable_webpage_preview=True,
            reply_markup=get_pagination(
                action="top",
                page=callback_data.page,
                pages_amount=callback_data.pages_amount,
                steam_id=callback_data.steam_id,
                steam_name=callback_data.steam_name,
            ),
        )
    elif callback_data.action == "info" or callback_data.action == "back":
        await callback.message.answer(
            text=f"Аккаунт {steam_name}\n"
            f"Количество предметов на аккаунте: {amount}\n"
            f"Общая стоимость предметов на аккаунте: {total_cost}руб.\n"
            f"Первоначальная стоимость предметов на аккаунте: {first_total_cost}руб.\n"
            f"Прирост стоимости: {difference_total_cost}руб.({int((difference_total_cost/first_total_cost)*100)}%)\n"
            f"Максимальная стоимость предмета: {max_cost} \n"
            f"Минимальная стоимость предмета: {min_cost}",
            disable_webpage_preview=True,
            reply_markup=get_items_menu(
                steam_id=callback_data.steam_id,
                steam_name=callback_data.steam_name,
            ),
        )
