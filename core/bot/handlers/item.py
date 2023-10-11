from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from urllib.parse import quote


from core.db.methods.request import (
    get_amount_and_items_info_from_db,
)


from core.bot.keyboards.inline import (
    get_items_menu,
)

router = Router()


@router.callback_query(F.data.startswith("inventory_"))
async def show_info_for_items(callback: CallbackQuery, session: AsyncSession):
    """Show info for current stream id"""
    inventory_info_data = callback.data.split("_")
    steamid_id = int(inventory_info_data[2])
    items_info = await get_amount_and_items_info_from_db(
        steam_id=steamid_id, session=session
    )
    total_cost = 0
    first_total_cost = 0
    amount = 0
    max_cost = 0
    min_cost = 10000000
    all_items_dict = []
    all_items_str = ""
    for item in items_info:
        cost = item.amount * item.steam_item.item_cost
        first_cost = item.amount * item.steam_item.first_item_cost
        total_cost += cost
        first_total_cost += first_cost
        amount += 1
        if item.steam_item.item_cost > max_cost:
            max_cost = item.steam_item.item_cost
        if 0 < item.steam_item.item_cost < min_cost:
            min_cost = item.steam_item.item_cost
        difference = item.steam_item.item_cost - item.steam_item.first_item_cost
        all_items_dict.append(
            {
                "name": item.steam_item.name,
                "cost": item.steam_item.item_cost,
                "first_cost": item.steam_item.first_item_cost,
                "diff": difference,
                "store": f"https://steamcommunity.com/market/listings/730/{quote(item.steam_item.name)}",
            }
        )
    for data in all_items_dict[0:5]:
        all_items_str += f'{data["name"]}\nПервоначальная стоимость:{data["first_cost"]}\nТекущая стоимость предмета {data["cost"]}\nПрирост стоимости {data["diff"]}\n Ссылка на торговую площадку:{data["store"]}\n\n'

    await callback.message.answer(
        text=f"Количество предметов на аккаунте: {all_items_str}\nОбщая стоимость предметов на аккаунте: {total_cost} \nПервоначальная стоимость предметов на аккаунте: {first_total_cost}\nМаксимальная стоимость предмета: {max_cost} \nМинимальная стоимость предмета: {min_cost}",
        reply_markup=get_items_menu(steam_id=steamid_id),
    )
    await callback.answer()


# @router.callback_query(F.data.startswith("items_list_"))
# async def show_info_for_items(callback: CallbackQuery, session: AsyncSession):
#     """Show info for current stream id"""
#     inventory_info_data = callback.data.split("_")
#     steamid_id = int(inventory_info_data[3])
#     items_info = await get_items_info_from_db(steam_id=steamid_id, session=session)
#     await callback.message.answer(
#         text=f"Количество предметов на аккаунте: {items_info}",
#         reply_markup=get_items_menu(steam_id=steamid_id),
#     )
#     await callback.answer()
