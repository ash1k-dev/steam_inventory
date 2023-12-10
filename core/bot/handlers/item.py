from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils import markdown


from urllib.parse import quote


from core.db.methods.request import (
    get_amount_and_items_info_from_db,
    get_items_info_from_db,
)


from core.bot.keyboards.inline.callback_factory import ItemsCallbackFactory

from core.bot.keyboards.inline.inline import (
    get_items_menu,
    get_pagination,
    get_items_back_menu,
)


from redis_data_convert import redis_convert_to_dict

router = Router()


@router.callback_query(ItemsCallbackFactory.filter())
async def get_items(
    callback: CallbackQuery,
    callback_data: ItemsCallbackFactory,
    session: AsyncSession,
):
    if callback_data.action == "info" or callback_data.action == "back":
        steam_id = callback_data.steam_id
        steam_name = callback_data.steam_name
        user_data = redis_convert_to_dict(f"{callback.from_user.id}")
        if user_data:
            items_info = user_data["steam_id"][f"{steam_id}"]["items_info"]
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
    else:
        if callback_data.action == "all":
            all_items = await get_amount_and_items_info_from_db(
                steam_id=callback_data.steam_id,
                limit=10000,
                order="all",
                session=session,
            )
        elif callback_data.action == "top_cost":
            all_items = await get_amount_and_items_info_from_db(
                steam_id=callback_data.steam_id, order="top_cost", session=session
            )
        elif callback_data.action == "top_gain":
            all_items = await get_amount_and_items_info_from_db(
                steam_id=callback_data.steam_id, order="top_gain", session=session
            )
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
        for i in range(0, len(items_list), 5):
            grouped_items_list.append("".join(items_list[i : i + 5]))
        if len(items_list) <= 5:
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
