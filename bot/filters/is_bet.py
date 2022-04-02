import re
from typing import Callable, Union

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data


class IsBet(BoundFilter):
    async def check(self, message: types.Message) -> "Union[bool, dict[str, list[tuple[int, str]]]]":
        match: Callable[[str], Union[re.Match, None]] = lambda text: re.match(r'^([0-9_,]+) (на )?([1-6]|([1-6]-[1-6]))$', text)

        # remove command at the beginning `!ставка 100 1`
        text = message.text.replace("!ставка ", '').replace("!с ", '').split('\n')

        if len(text) > 10:
            return False

        if not all([match(bet) for bet in text]):
            return False

        bets = []
        for bet in text:
            amount, *args, numbers = bet.split()
            amount = amount.replace('_', '').replace(',', '')
            if amount == '':    # check if bet is not like '__ 1' 
                return False
            
            if int(amount) == 0:
                return False

            if len(numbers) > 1 and numbers[2] <= numbers[0]:
                return False 

            bets.append((amount, numbers))


        return {"bets": bets}
