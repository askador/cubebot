from pprint import pprint
from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.utils.misc.throttling import rate_limit
from bot.types import I18nJSON


# @rate_limit(5, 'echo')
async def bot_echo(message: types.Message, i18n: I18nJSON):
    name = message.from_user.full_name
    await message.answer(await i18n.t('start', {"name": name}))
