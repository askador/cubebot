import re
from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsBet(BoundFilter):
    async def check(self, message: types.Message) -> Union[bool, dict[str, dict]]:
        # remove command at the beginning
        text = message.text.replace("!ставка ", '').replace("!с ", '')

        if re.match(r'^([0-9_,]+) (на )?([1-6]|([1-6]-[1-6]))$', text) is None:
            return False
            
        amount = text.split()[0].replace('_', '').replace(',', '')
        numbers = text.split()[-1]
        
        if amount == '': # check if bet is not like '__ 1' 
            return False

        if int(amount) <= 0:
            return False

        if len(numbers) > 1 and numbers[2] <= numbers[0]:
            return False 

        return {"bet_data": {"amount": int(amount), "numbers": numbers}}