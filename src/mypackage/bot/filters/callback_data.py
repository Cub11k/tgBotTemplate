from typing import Union

from telebot.types import CallbackQuery
from telebot.custom_filters import AdvancedCustomFilter


# Convenient way to filter callback_data instead of using lambda functions
class CallbackDataFilter(AdvancedCustomFilter):
    key = 'cb_data'

    # argument naming is kept from the base class to avoid possible errors if passed as kwargs
    # message is an update, text is a value passed to the filter on handler registration
    def check(self, message: CallbackQuery, text: Union[str, list]):
        if isinstance(text, list):
            # exact match with any of the texts
            return message.data in text
        elif isinstance(text, str):
            # exact match with the text
            return message.data == text
        else:
            # unexpected type
            return False
