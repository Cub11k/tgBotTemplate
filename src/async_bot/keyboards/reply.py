from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from async_bot.config import ReplyButtons


class ReplyKeyboards:
    def __init__(self, buttons: ReplyButtons):
        self.buttons = buttons

    @property
    def remove(self):
        return ReplyKeyboardRemove()
