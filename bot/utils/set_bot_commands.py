from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import Bot


async def set_bot_commands(bot: Bot):
    data = [
        (
            [
                BotCommand("start", "New Game"),
                BotCommand("help", "How to play Bombsweeper?"),
                BotCommand("stats", "Your personal statistics")
            ],
            BotCommandScopeDefault(),
            None
        )
    ]
    for commands_list, commands_scope, language in data:
        await bot.set_my_commands(commands=commands_list, scope=commands_scope, language_code=language)

