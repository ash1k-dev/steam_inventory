from urllib.parse import quote

from aiogram import Router
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from config import ITEMS_ON_PAGE, URL_FOR_STEAM_ITEM
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot.handlers.templates import TEXT_ITEMS_INFO, TEXT_ITEMS
from core.bot.keyboards.inline.callback_factory import ItemsCallbackFactory
from core.bot.keyboards.inline.inline import (
    get_items_back_menu,
    get_items_menu,
    get_pagination,
)
from core.db.methods.request import (
    get_items_info_from_redis_or_db,
    get_items_list_from_redis_or_db,
)

router = Router()


@router.callback_query(ItemsCallbackFactory.filter())
async def get_items(
    callback: CallbackQuery,
    callback_data: ItemsCallbackFactory,
    session: AsyncSession,
    storage: RedisStorage,
):
    if callback_data.action == "info" or callback_data.action == "back":
        (
            difference_total_cost,
            first_total_cost,
            max_cost,
            min_cost,
            total_amount,
            total_cost,
        ) = await get_items_info_from_redis_or_db(
            session=session,
            callback_data=callback_data,
            telegram_id=callback.from_user.id,
            storage=storage,
        )
        await callback.message.answer(
            text=TEXT_ITEMS_INFO.substitute(
                steam_name=callback_data.steam_name,
                total_amount=total_amount,
                total_cost=total_cost,
                first_total_cost=first_total_cost,
                difference_total_cost=difference_total_cost,
                difference_percents=int(
                    (difference_total_cost / first_total_cost) * 100
                ),
                max_cost=max_cost,
                min_cost=min_cost,
            ),
            reply_markup=get_items_menu(
                steam_id=callback_data.steam_id,
                steam_name=callback_data.steam_name,
            ),
        )
    else:
        if callback_data.action == "all":
            items = await get_items_list_from_redis_or_db(
                callback_data=callback_data,
                session=session,
                telegram_id=callback.from_user.id,
                storage=storage,
                order="cost",
            )
        elif callback_data.action == "top_cost":
            items = await get_items_list_from_redis_or_db(
                callback_data=callback_data,
                session=session,
                telegram_id=callback.from_user.id,
                storage=storage,
                order="cost",
            )
        elif callback_data.action == "top_gain":
            items = await get_items_list_from_redis_or_db(
                callback_data=callback_data,
                session=session,
                telegram_id=callback.from_user.id,
                storage=storage,
                order="difference",
            )
        grouped_items_list, items_list = await get_items_text(items)
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


async def get_items_text(items):
    items_list = []
    grouped_items_list = []
    for item_name, item_cost, first_item_cost, amount, difference in items:
        if first_item_cost != 0:
            items_list.append(
                TEXT_ITEMS.substitute(
                    item_name=item_name,
                    item_cost=item_cost,
                    first_item_cost=first_item_cost,
                    difference=difference,
                    difference_percents=int(difference / first_item_cost * 100),
                    amount=amount,
                    link=markdown.hlink(
                        "SteamLink", f"{URL_FOR_STEAM_ITEM}/{quote(item_name)}"
                    ),
                )
            )
    return grouped_items_list, items_list
