from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeAllPrivateChats
from aiogram import Bot


DEFAULT_SCOPE_COMMANDS = (
    [
        BotCommand("start", "Приветственное сообщение"),
        BotCommand("help", "Помощь"),
        BotCommand("game", "Начать новую игру"),
        BotCommand("roll", "Бросить кости"),
        BotCommand("logs", "Логи 10 предыдущих игр"),
        # BotCommand("rating", "Рейтинг по чату"),
        BotCommand("money", "Просмотреть баланс"),
        BotCommand("profile", "Профиль игрока"),
    ],
    BotCommandScopeDefault(),
    None
)

EN_SCOPE_COMMANDS = (
    [
        BotCommand("start", "Greeting message"),
        BotCommand("help", "Help message"),
        BotCommand("game", "Start a new game"),
        BotCommand("roll", "Roll the dice"),
        BotCommand("logs", "Logs of 10 previous games"),
        # BotCommand("rating", "Rating"),
        BotCommand("money", "Current player money"),
        BotCommand("profile", "Player Profile"),
    ],
    BotCommandScopeDefault(),
    'en'
)

PRIVATE_CHAT_DEFAULT_SCOPE_COMMANDS = (
    [
        BotCommand("start", "Приветственное сообщение"),
        BotCommand("help", "Помощь"),
        BotCommand("game", "Начать новую игру"),
        BotCommand("roll", "Бросить кости"),
        BotCommand("logs", "Логи 10 предыдущих игр"),
        BotCommand("money", "Просмотреть баланс"),
        BotCommand("profile", "Профиль игрока"),
        BotCommand("issue", "Сообщить о проблеме с ботом"),
    ],
    BotCommandScopeAllPrivateChats(),
    None
)

PRIVATE_CHAT_EN_SCOPE_COMMANDS = (
    [
        BotCommand("start", "Greeting message"),
        BotCommand("help", "Help message"),
        BotCommand("game", "Start a new game"),
        BotCommand("roll", "Roll the dice"),
        BotCommand("logs", "Logs of 10 previous games"),
        BotCommand("money", "Current player money"),
        BotCommand("profile", "Player Profile"),
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
