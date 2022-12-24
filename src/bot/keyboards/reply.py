from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from bot.config.models import ReplyButtons


class ReplyKeyboards:
    def __init__(self, buttons: ReplyButtons):
        self.buttons = buttons

    @property
    def remove(self):
        return ReplyKeyboardRemove()
