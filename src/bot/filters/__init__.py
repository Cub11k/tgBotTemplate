from telebot import TeleBot
from telebot.custom_filters import StateFilter

from storages import Storage

from bot.config import Config
from bot.logger import Logger


def add_custom_filters(bot: TeleBot, cfg: Config, storage: Storage, logger: Logger):
    bot.add_custom_filter(StateFilter(bot))


__all__ = (
    "add_custom_filters",
)
