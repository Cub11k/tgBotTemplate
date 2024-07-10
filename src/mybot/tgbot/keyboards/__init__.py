from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import ReplyKeyboardRemove


# TODO: define all keyboards and/or keyboard builders here or in the submodules of this module

def help_reply_keyboard(help_btn: str):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(help_btn))
    return keyboard


def empty_inline():
    return InlineKeyboardMarkup()


def empty_reply():
    return ReplyKeyboardMarkup()


def remove_reply():
    return ReplyKeyboardRemove()
