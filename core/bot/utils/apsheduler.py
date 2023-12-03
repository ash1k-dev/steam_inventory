from aiogram import Bot
from aiogram.utils import markdown
from sqlalchemy.ext.asyncio import async_sessionmaker


from config import DEPRECIATION_FACTOR, INCREASE_FACTOR


from methods.request import (
    get_all_tracking_items_from_db,
    get_all_tracking_games_from_db,
    get_all_user_from_db,
    get_all_steam_ids_from_db,
    get_amount_and_items_info_from_db,
)

from urllib.parse import quote


from methods.update import update_all_items, update_all_games


async def check_update(bot: Bot, sessionmaker: async_sessionmaker) -> None:
    async with sessionmaker() as session:
        await update_all_items(session=session)
        await update_all_games(session=session)
        all_users = await get_all_user_from_db(session=session)
        for user in all_users:
            await get_items_changes(
                bot=bot, user_telegram_id=user.telegram_id, session=session
            )
            await get_tracking_items_changes(
                bot=bot, user_telegram_id=user.telegram_id, session=session
            )

            await get_tracking_game_changes(
                bot=bot,
                user_telegram_id=user.telegram_id,
                session=session,
            )


async def get_items_changes(bot, session, user_telegram_id):
    all_steam_ids = await get_all_steam_ids_from_db(
        telegram_id=user_telegram_id, session=session
    )
    for steam_id in all_steam_ids:
        items = f"Подорожавшие предметы на аккаунте {steam_id.name}:\n\n"
        items_info = await get_amount_and_items_info_from_db(
            steam_id=steam_id.steam_id, session=session
        )
        for item in items_info:
            name, item_cost, first_item_cost, _ = item
            difference_for_item = item_cost - first_item_cost
            if item_cost > first_item_cost * float(INCREASE_FACTOR):
                items += (
                    f"Название предмета: {name} \n"
                    f"Первоначальная стоимость: {first_item_cost} \n"
                    f"Актуальная стоимость: {item_cost} \n"
                    f"Прирост: +{difference_for_item} руб. (+{int((difference_for_item / first_item_cost) * 100)}%)\n"
                    f"Ссылка на предмет:"
                    f" {markdown.hlink('SteamLink', f'https://steamcommunity.com/market/listings/730/{quote(name)}')} \n\n\n"
                )
        if items != f"Подорожавшие предметы на аккаунте {steam_id.name}:\n\n":
            await bot.send_message(
                chat_id=user_telegram_id,
                disable_web_page_preview=True,
                text=items,
            )


async def get_tracking_items_changes(bot, session, user_telegram_id):
    all_tracking_items = await get_all_tracking_items_from_db(
        telegram_id=user_telegram_id, session=session
    )
    tracking_items = "Подешевевшие предметы:\n\n"
    for tracking_item in all_tracking_items:
        name, first_item_cost, _, item_id, item_cost = tracking_item
        difference_for_tracking_items = first_item_cost - item_cost
        if item_cost < first_item_cost * float(DEPRECIATION_FACTOR):
            tracking_items += (
                f"Название предмета: {name} \n"
                f"Первоначальная стоимость: {first_item_cost} \n"
                f"Актуальная стоимость: {item_cost} \n"
                f"Понижение: -{difference_for_tracking_items} руб.(-{int((difference_for_tracking_items / first_item_cost) * 100)}%) \n"
                f"Ссылка на предмет:"
                f" {markdown.hlink('SteamLink', f'https://steamcommunity.com/market/listings/730/{quote(name)}')} \n\n\n"
            )
    if tracking_items != "Подешевевшие предметы:\n\n":
        await bot.send_message(
            chat_id=user_telegram_id,
            disable_web_page_preview=True,
            text=tracking_items,
        )


async def get_tracking_game_changes(bot, user_telegram_id, session):
    all_tracking_games = await get_all_tracking_games_from_db(
        telegram_id=user_telegram_id, session=session
    )
    tracking_games = "Подешевевшие игры:\n\n"
    for tracking_game in all_tracking_games:
        _, name, game_id, first_game_cost, game_cost = tracking_game
        difference_for_tracking_games = first_game_cost - game_cost
        if game_cost < first_game_cost * float(DEPRECIATION_FACTOR):
            tracking_games += (
                f"Название игры: {name} \n"
                f"Первоначальная стоимость: {first_game_cost} \n"
                f"Актуальная стоимость: {game_cost} \n"
                f"Изменение: -{difference_for_tracking_games} руб.(-{int((difference_for_tracking_games / first_game_cost) * 100)}%) \n"
                f"Ссылка на игру: "
                f"{markdown.hlink('SteamLink', f'https://store.steampowered.com/app/{game_id}')}\n\n"
            )
    if tracking_games != "Подешевевшие игры:\n\n":
        await bot.send_message(
            chat_id=user_telegram_id,
            disable_web_page_preview=True,
            text=tracking_games,
        )
