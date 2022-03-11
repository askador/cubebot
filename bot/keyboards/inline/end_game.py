from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

def play_again_kb(locale: str = 'ru') -> InlineKeyboardMarkup:
    locales = {
        "ru": "Играть снова",
        "en": "Play again"
    }

    cd = CallbackData('game', 'action')
    play_again = locales.get(locale, "Бросить")

    kb = [
        [
            InlineKeyboardButton(
                play_again,
                callback_data=cd.new(action='play_again')
            ),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
