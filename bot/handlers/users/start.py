from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from bot.states import Form


async def start(message: types.Message):
    await Form.name.set()

    await message.reply("Hi there! What's your name?")


async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.reply("How old are you?")

async def process_age_invalid(message: types.Message):
    """
    If age is invalid
    """
    return await message.reply("Age gotta be a number.\nHow old are you? (digits only)")

async def process_age(message: types.Message, state: FSMContext):
    # Update state and data
    await Form.next()
    await state.update_data(age=int(message.text))

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Male", "Female")
    markup.add("Other")

    await message.reply("What is your gender?", reply_markup=markup)


async def process_gender_invalid(message: types.Message):
    """
    In this example gender has to be one of: Male, Female, Other.
    """
    return await message.reply("Bad gender name. Choose your gender from the keyboard.")


async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text

        # Remove keyboard
        markup = types.ReplyKeyboardRemove()

        # And send message 
        await message.answer(
            data,
            reply_markup=markup,
        )

    # Finish conversation
    await state.reset_state(with_data=False)