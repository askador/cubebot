from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def new_game_kb() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton("100 на 1", callback_data="ставка 100-1"),
            InlineKeyboardButton("100 на 2", callback_data="ставка 100-2"),
            InlineKeyboardButton("100 на 3", callback_data="ставка 100-3"),
        ],
        [
            InlineKeyboardButton("100 на 4", callback_data="ставка 100-4"),
            InlineKeyboardButton("100 на 5", callback_data="ставка 100-5"),
            InlineKeyboardButton("100 на 6", callback_data="ставка 100-6"),
        ],
    ]


    return InlineKeyboardMarkup(inline_keyboard=kb)