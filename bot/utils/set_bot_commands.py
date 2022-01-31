from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import Bot


async def set_bot_commands(bot: Bot):
    data = [
        (
            [
                BotCommand("start", "Приветственное сообщение"),
                BotCommand("help", "Помощь"),
                BotCommand("game", "Начать новую игру"),
                BotCommand("roll", "Бросить кости"),
                BotCommand("money", "Просмотреть баланс"),
                BotCommand("profile", "Профиль игрока"),
                BotCommand("issue", "Сообщить о проблеме с ботом"),
            ],
            BotCommandScopeDefault(),
            None
        )
    ]
    for commands_list, commands_scope, language in data:
        await bot.set_my_commands(commands=commands_list, scope=commands_scope, language_code=language)

