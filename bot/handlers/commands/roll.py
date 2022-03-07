import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from sqlalchemy import select, func, text, delete, update, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util._collections import immutabledict

from bot.db.models import Bet, Player, Game, ChatLog
from bot.filters import StrictCommand, CanRoll
from bot.types.Localization import I18nJSON
from bot.utils import rate_limit
from bot.analytics import analytics
from bot.analytics.events import EventAction, EventCommand


@rate_limit("roll")
@analytics.command(EventCommand.ROLL)
async def roll(
    message: types.Message, 
    i18n: I18nJSON, 
    session: AsyncSession,
    no_bets: bool = False
):
    # if player has no bets. Taken from filter
    if no_bets:
        await analytics.action(message.chat.id, EventAction.SEND_MESSAGE)
        return await message.reply(i18n.t('commands.roll.invalid'))

    await session.execute(update(Game).where(Game.chat_id == message.chat.id).values({"is_rolling": True}))
    await session.commit()

    dice_msg = await message.answer_dice("🎲")
    await analytics.action(message.chat.id, EventAction.SEND_MESSAGE)
    number = dice_msg.dice.value

    results = f'🎲  {number}\n'
    results += await process_bets(number, message.chat.id, session, i18n)

    await asyncio.sleep(4)
    await message.answer(results)
    await analytics.action(message.chat.id, EventAction.SEND_MESSAGE)


async def process_bets(number, chat_id, session: AsyncSession, i18n: I18nJSON) -> str:
    query = select([Bet.player_id,Bet.numbers, func.sum(Bet.amount).label("amount")]) \
        .where(Bet.chat_id == chat_id) \
        .group_by(Bet.player_id, Bet.chat_id, Bet.numbers)

    bets: list[Bet] = (await session.execute(query)).all()

    all_bets = i18n.t('commands.roll.results.all_bets_label')
    results = i18n.t('commands.roll.results.results_label')

    for bet in bets:
        prize = 0

        player: Player = await session.get(Player, bet.player_id)
        await update_player_stats(player, {"plays_amount": 1})

        # check winning bet
        if len(bet.numbers) > 1:
            if int(bet.numbers[0]) <= number <= int(bet.numbers[2]):
                prize = int(bet.amount * 6 / (int(bet.numbers[2]) - int(bet.numbers[0]) + 1))
        else:   
            if int(bet.numbers) == number:
                prize = int(bet.amount * 6)

        # update player 
        if prize > 0:
            await update_player_stats(player, {"won": prize})

            player.money += prize
            results += i18n.t('commands.roll.results.won', {
                "id": player.id,
                "name": player.fullname,
                "prize": f"{prize:,}",
                "numbers": bet.numbers
            }, amount=prize)

        else:
            await update_player_stats(player, {"loss": bet.amount})


        all_bets += i18n.t('commands.roll.results.all_bets', {
            "name": player.fullname,
            "amount": f"{bet.amount:,}",
            "numbers": bet.numbers
        }, amount=bet.amount)


    await session.execute(delete(Bet).where(Bet.chat_id == chat_id))
    await session.execute(delete(Game).where(Game.chat_id == chat_id))
    await add_chat_log(chat_id, number, session)
    await session.commit()

    return all_bets + "\n" + results
    

async def update_player_stats(player: Player, stats: "dict[str, int]") -> None:
    player.won          += stats.get("won", 0)                      
    player.plays_amount += stats.get("plays_amount", 0)             
    player.loss         += stats.get("loss", 0)                     


async def add_chat_log(chat_id, number, session: AsyncSession) -> None:
    logs_max_count = 10

    session.add(ChatLog(chat_id=chat_id, log=str(number)))
    await session.commit()

    count = (await session.execute(
        select(func.count(ChatLog.id)).where(ChatLog.chat_id==chat_id)
    )).fetchone()[0]

    if count > logs_max_count:
        stmt = select([ChatLog.id]).order_by(desc(ChatLog.id)).limit(logs_max_count)
        await session.execute(
            delete(ChatLog).where(ChatLog.id.notin_(stmt)), 
            execution_options=immutabledict({"synchronize_session": 'fetch'})
        )


def register(dp: Dispatcher):
    dp.register_message_handler(roll, Command('roll'), StrictCommand(), CanRoll()) 
