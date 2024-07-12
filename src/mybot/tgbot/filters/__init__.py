from telebot import TeleBot
from telebot.custom_filters import StateFilter


from .callback_data import CallbackDataFilter
from .text import TextEqualsFilter
from .roles import IsOwnerFilter


def add_custom_filters(bot: TeleBot, owner_tg_id: int):
    # TODO: add any custom filters here
    bot.add_custom_filter(StateFilter(bot))
    bot.add_custom_filter(TextEqualsFilter())
    bot.add_custom_filter(CallbackDataFilter())
    bot.add_custom_filter(IsOwnerFilter(owner_tg_id))
