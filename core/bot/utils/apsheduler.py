from urllib.parse import quote

from aiogram import Bot
from aiogram.utils import markdown
from methods.request import get_all_user_from_db, get_changes
from methods.update import update_all_items_and_games, update_redis
from sqlalchemy.ext.asyncio import async_sessionmaker


async def check_update(bot: Bot, sessionmaker: async_sessionmaker, storage) -> None:
    async with sessionmaker() as session:
        # await update_all_items_and_games(session)
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
        tracking_items_info = await check_tracking_items(tracking_items)
        if tracking_items_info:
            await bot.send_message(
                chat_id=user_telegram_id,
                disable_web_page_preview=True,
                text=tracking_items_info,
            )
    if tracking_games:
        tracking_games_info = await check_tracking_games(tracking_games)
        if tracking_games_info:
            await bot.send_message(
                chat_id=user_telegram_id,
                disable_web_page_preview=True,
                text=tracking_games_info,
            )
    if items:
        for steam_id, item_data in items.items():
            items_info = await check_items(item_data, steam_id)
            if items_info:
                await bot.send_message(
                    chat_id=user_telegram_id,
                    disable_web_page_preview=True,
                    text=items_info,
                )


async def check_items(item_data, steam_id):
    items_info = f"Подорожавшие предметы на аккаунте {steam_id}:\n\n"
    for name, item_cost, first_item_cost in item_data:
        difference_for_item = item_cost - first_item_cost
        items_info += (
            f"Название предмета: {name} \n"
            f"Первоначальная стоимость: {first_item_cost} \n"
            f"Актуальная стоимость: {item_cost} \n"
            f"Прирост: +{difference_for_item} руб. "
            f"(+{int((difference_for_item / first_item_cost) * 100)}%)\n"
            f"Ссылка на предмет:"
            f" {markdown.hlink('SteamLink', f'https://steamcommunity.com/market/listings/730/{quote(name)}')} \n\n"
        )
    if items_info != f"Подорожавшие предметы на аккаунте {steam_id}:\n\n":
        return items_info


async def check_tracking_games(tracking_games):
    tracking_games_info = "Подешевевшие игры:\n\n"
    for name, game_id, first_game_cost, game_cost in tracking_games:
        difference_for_tracking_games = first_game_cost - game_cost
        tracking_games_info += (
            f"Название игры: {name} \n"
            f"Первоначальная стоимость: {first_game_cost} \n"
            f"Актуальная стоимость: {game_cost} \n"
            f"Изменение: -{difference_for_tracking_games} руб."
            f"(-{int((difference_for_tracking_games / first_game_cost) * 100)}%) \n"
            f"Ссылка на игру: "
            f"{markdown.hlink('SteamLink', f'https://store.steampowered.com/app/{game_id}')}\n\n"
        )
    if tracking_games_info != "Подешевевшие игры:\n\n":
        return tracking_games_info


async def check_tracking_items(tracking_items):
    tracking_items_info = "Подешевевшие предметы:\n\n"
    for name, item_id, first_item_cost, item_cost in tracking_items:
        difference = first_item_cost - item_cost
        tracking_items_info += (
            f"Название предмета: {name} \n"
            f"Первоначальная стоимость: {first_item_cost} \n"
            f"Актуальная стоимость: {item_cost} \n"
            f"Понижение: -{difference} "
            f"руб.(-{int((difference / first_item_cost) * 100)}%) \n"
            f"Ссылка на предмет:"
            f" {markdown.hlink('SteamLink', f'https://steamcommunity.com/market/listings/730/{quote(name)}')} \n\n\n"
        )
    if tracking_items_info != "Подешевевшие предметы:\n\n":
        return tracking_items_info
