from telebot import TeleBot
from telebot.custom_filters import StateFilter

from bot.config import Config
from bot.logger import Logger
from bot.storages import Storage


def add_filters(bot: TeleBot, cfg: Config, storage: Storage, logger: Logger):
    bot.add_custom_filter(StateFilter(bot))


__all__ = (
    "add_filters",
)
