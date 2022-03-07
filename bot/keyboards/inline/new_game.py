from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


def new_game_kb(locale: str = 'ru') -> InlineKeyboardMarkup:
    bet_locales = {
        "ru": "{amount} на {number}",
        "en": "{amount} on {number}"
    }

    roll_locales = {
        "ru": "Бросить",
        "en": "Roll"
    }

    bet_cd = CallbackData('game', 'action', 'amount', 'number')
    roll_cd = CallbackData('game', 'action')
    bet = bet_locales.get(locale, "{amount} на {number}")
    roll = roll_locales.get(locale, "Бросить")

    kb = [
        [
            InlineKeyboardButton(
                bet.format(amount=100, number=1),
                callback_data=bet_cd.new(action='bet', amount=100, number='1')
            ),
            InlineKeyboardButton(
                bet.format(amount=100, number=2),
                callback_data=bet_cd.new(action='bet', amount=100, number='2')
            ),
            InlineKeyboardButton(
                bet.format(amount=100, number=3),
                callback_data=bet_cd.new(action='bet', amount=100, number='3')
            ),
        ],
        [
            InlineKeyboardButton(
                bet.format(amount=100, number=4),
                callback_data=bet_cd.new(action='bet', amount=100, number='4')
            ),
            InlineKeyboardButton(
                bet.format(amount=100, number=5),
                callback_data=bet_cd.new(action='bet', amount=100, number='5')
            ),
            InlineKeyboardButton(
                bet.format(amount=100, number=6),
                callback_data=bet_cd.new(action='bet', amount=100, number='6')
            ),
        ],
        [
            InlineKeyboardButton(
                roll,
                callback_data=roll_cd.new(action='roll')
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
