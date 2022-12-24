from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.callback_data import CallbackData, CallbackDataFilter

from bot.config.models import InlineButtons


class InlineKeyboards:
    def __init__(self, buttons: InlineButtons):
        self.buttons = buttons

    @property
    def remove(self):
        return InlineKeyboardMarkup()
