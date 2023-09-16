from typing import Union

from telebot.types import Message
from telebot.custom_filters import AdvancedCustomFilter


class TextEqualsFilter(AdvancedCustomFilter):
    key = 'text_equals'

    # argument naming is kept from the base class to avoid possible errors if passed as kwargs
    # message is an update, text is a value passed to the filter on handler registration
    def check(self, message: Message, text: Union[str, list]):
        if isinstance(text, list):
            # check if the text is in the list
            return message.text in text
        elif isinstance(text, str):
            # exact match of the text
            return message.text == text
        else:
            # unexpected type
            return False
