from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeAllPrivateChats
from aiogram import Bot


DEFAULT_SCOPE_COMMANDS = (
    [
        BotCommand("start", "Приветственное сообщение"),
        BotCommand("game", "Начать новую игру"),
        BotCommand("roll", "Бросить кости"),
        BotCommand("profile", "Профиль игрока"),
        BotCommand("logs", "Логи 10 предыдущих игр"),
        BotCommand("help", "Помощь"),
        # BotCommand("rating", "Рейтинг по чату"),
        BotCommand("money", "Просмотреть баланс"),
    ],
    BotCommandScopeDefault(),
    None
)

EN_SCOPE_COMMANDS = (
    [
        BotCommand("start", "Greeting message"),
        BotCommand("game", "Start a new game"),
        BotCommand("roll", "Roll the dice"),
        BotCommand("profile", "Player Profile"),
        BotCommand("logs", "Logs of 10 previous games"),
        BotCommand("help", "Help message"),
        # BotCommand("rating", "Rating"),
        BotCommand("money", "Current player money"),
    ],
    BotCommandScopeDefault(),
    'en'
)

PRIVATE_CHAT_DEFAULT_SCOPE_COMMANDS = (
    [
        BotCommand("start", "Приветственное сообщение"),
        BotCommand("game", "Начать новую игру"),
        BotCommand("roll", "Бросить кости"),
        BotCommand("profile", "Профиль игрока"),
        BotCommand("logs", "Логи 10 предыдущих игр"),
        BotCommand("help", "Помощь"),
        BotCommand("money", "Просмотреть баланс"),
        BotCommand("issue", "Сообщить о проблеме с ботом"),
    ],
    BotCommandScopeAllPrivateChats(),
    None
)

PRIVATE_CHAT_EN_SCOPE_COMMANDS = (
    [
        BotCommand("start", "Greeting message"),
        BotCommand("game", "Start a new game"),
        BotCommand("roll", "Roll the dice"),
        BotCommand("profile", "Player Profile"),
        BotCommand("logs", "Logs of 10 previous games"),
        BotCommand("money", "Current player money"),
        BotCommand("help", "Help message"),
        BotCommand("issue", "Report an issue with bot"),
    ],
    BotCommandScopeAllPrivateChats(),
    'en'
)


async def set_bot_commands(bot: Bot):

    commands = [
        EN_SCOPE_COMMANDS,
        DEFAULT_SCOPE_COMMANDS,
        PRIVATE_CHAT_EN_SCOPE_COMMANDS,
        PRIVATE_CHAT_DEFAULT_SCOPE_COMMANDS
    ]

    for commands_list, commands_scope, language in commands:
        await bot.set_my_commands(commands=commands_list, scope=commands_scope, language_code=language)
