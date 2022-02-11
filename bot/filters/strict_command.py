from aiogram import types
from aiogram.dispatcher.filters import BoundFilter



class StrictCommand(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        if message.chat.type == 'private':
            return True

        if not message.is_command():
            return False

        full_command, *args_list = message.text.split(maxsplit=1)
        command, _, mention = full_command[1:].partition('@')

        if mention == (await message.bot.me).username:
            return True

        return False
