from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart

from bot.states import Form

from .start import start, process_age, process_age_invalid, process_gender, process_gender_invalid, process_name

from .echo import bot_echo
 

def register_users_handlers(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart())

    dp.register_message_handler(process_name, state=Form.name)
    dp.register_message_handler(process_age_invalid, lambda message: not message.text.isdigit(), state=Form.age)
    dp.register_message_handler(process_age, lambda message: message.text.isdigit(), state=Form.age)
    dp.register_message_handler(process_gender_invalid, lambda message: message.text not in ["Male", "Female", "Other"], state=Form.gender)
    dp.register_message_handler(process_gender, state=Form.gender)

    dp.register_message_handler(bot_echo)
