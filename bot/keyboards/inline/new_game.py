from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


def new_game_kb(locale: str = 'ru') -> InlineKeyboardMarkup:
    locales = {
        "ru": "{amount} на {number}",
        "en": "{amount} on {number}"
    }

    cd = CallbackData('game', 'action', 'amount', 'number')
    line = locales.get(locale, "{amount} на {number}")

    kb = [
        [
            InlineKeyboardButton(
                line.format(amount=100, number=1),
                callback_data=cd.new(action='bet', amount=100, number='1')
            ),
            InlineKeyboardButton(
                line.format(amount=100, number=2),
                callback_data=cd.new(action='bet', amount=100, number='2')
            ),
            InlineKeyboardButton(
                line.format(amount=100, number=3),
                callback_data=cd.new(action='bet', amount=100, number='3')
            ),
        ],
        [
            InlineKeyboardButton(
                line.format(amount=100, number=4),
                callback_data=cd.new(action='bet', amount=100, number='4')
            ),
            InlineKeyboardButton(
                line.format(amount=100, number=5),
                callback_data=cd.new(action='bet', amount=100, number='5')
            ),
            InlineKeyboardButton(
                line.format(amount=100, number=6),
                callback_data=cd.new(action='bet', amount=100, number='6')
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
