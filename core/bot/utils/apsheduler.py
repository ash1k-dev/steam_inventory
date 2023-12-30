from urllib.parse import quote

from aiogram import Bot
from aiogram.utils import markdown
from methods.request import get_all_user_from_db, get_changes
from methods.update import update_all_items_and_games, update_redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import URL_FOR_STEAM_GAME, URL_FOR_STEAM_ITEM
from core.bot.utils.templates import TEXT_CHANGING


async def check_update(bot: Bot, sessionmaker: async_sessionmaker, storage) -> None:
    async with sessionmaker() as session:
        await update_all_items_and_games(session)
        all_users = await get_all_user_from_db(session=session)
        for user in all_users:
            await update_redis(
                user_telegram_id=user.telegram_id, session=session, storage=storage
            )
            changes_dict = await get_changes(
                user_telegram_id=user.telegram_id, session=session
            )
            await send_changes(
                bot=bot, user_telegram_id=user.telegram_id, changes_dict=changes_dict
            )


async def send_changes(bot, user_telegram_id, changes_dict):
    tracking_items, tracking_games, items = changes_dict
    if tracking_items:
        tracking_items_info = await check_tracking_items(tracking_items=tracking_items)
        if tracking_items_info:
            await bot.send_message(
                chat_id=user_telegram_id,
                disable_web_page_preview=True,
                text=f"Подешевевшие предметы:\n\n{tracking_items_info}",
            )
    if tracking_games:
        tracking_games_info = await check_tracking_games(tracking_games=tracking_games)
        if tracking_games_info:
            await bot.send_message(
                chat_id=user_telegram_id,
                disable_web_page_preview=True,
                text=f"Подешевевшие игры:\n\n{tracking_games_info}",
            )
    if items:
        for steam_id, item_data in items.items():
            items_info = await check_items(item_data=item_data)
            if items_info:
                await bot.send_message(
                    chat_id=user_telegram_id,
                    disable_web_page_preview=True,
                    text=f"Подорожавшие предметы на аккаунте {steam_id}:\n\n{items_info}",
                )


async def check_items(item_data):
    items_info = ""
    for name, item_cost, first_item_cost in item_data:
        difference_for_item = item_cost - first_item_cost
        items_info += TEXT_CHANGING.substitute(
            name=name,
            first_cost=first_item_cost,
            cost=item_cost,
            difference=difference_for_item,
            difference_percents=int((difference_for_item / first_item_cost) * 100),
            link=markdown.hlink("SteamLink", f"{URL_FOR_STEAM_ITEM}{quote(name)}"),
        )
    return items_info


async def check_tracking_games(tracking_games):
    tracking_games_info = ""
    for name, game_id, first_game_cost, game_cost in tracking_games:
        difference_for_tracking_games = game_cost - first_game_cost
        tracking_games_info += TEXT_CHANGING.substitute(
            name=name,
            first_cost=first_game_cost,
            cost=game_cost,
            difference=difference_for_tracking_games,
            difference_percents=int(
                (difference_for_tracking_games / first_game_cost) * 100
            ),
            link=markdown.hlink("SteamLink", f"{URL_FOR_STEAM_GAME}{game_id}"),
        )
    return tracking_games_info


async def check_tracking_items(tracking_items):
    tracking_items_info = ""
    for name, item_id, first_item_cost, item_cost in tracking_items:
        difference_for_tracking_items = item_cost - first_item_cost
        tracking_items_info += TEXT_CHANGING.substitute(
            name=name,
            first_cost=first_item_cost,
            cost=item_cost,
            difference=difference_for_tracking_items,
            difference_percents=int(
                (difference_for_tracking_items / first_item_cost) * 100
            ),
            link=markdown.hlink("SteamLink", f"{URL_FOR_STEAM_ITEM}{quote(name)}"),
        )
    return tracking_items_info
