import re

from aiogram import Dispatcher
from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import Command, ChatTypeFilter, IsReplyFilter
from sqlalchemy import update

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Player
from bot.types.Localization import I18nJSON


async def give_money(
    message: Message,
    command: Command.CommandObj,
    session: AsyncSession,
    player: Player,
    i18n: I18nJSON
):
    recipient = message.reply_to_message.from_user
    if recipient.is_bot:
        return

    amount = command.args
    if re.match(r'^[0-9_,]+$', amount) is None:
        return

    amount = amount.replace('_', '').replace(',', '')
    if amount == '' or int(amount) == 0:  # check if bet is not like '__ 1'
        return

    amount = int(amount)
    if amount >= player.money:
        return await message.answer(i18n.t('money.not_enough'))

    # add player if not exists
    await session.merge(Player(id=recipient.id, fullname=recipient.full_name))
    await session.commit()

    # adjust player's money 
    await session.execute(update(Player).where(Player.id == recipient.id).values(money=Player.money+amount))
    player.money -= amount
    await session.commit()

    await message.answer(i18n.t('commands.give_money', {
            "sender_id": player.id,
            "sender_name": player.fullname,
            "recipient_id": recipient.id,
            "recipient_name": recipient.full_name,
            "amount": f"{amount:,}"
        }, amount=amount))


def register(dp: Dispatcher):
    dp.register_message_handler(
        give_money,
        Command('передать', prefixes='!'),
        ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]),
        IsReplyFilter(True)
    )
