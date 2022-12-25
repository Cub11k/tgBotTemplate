from telebot import TeleBot
from telebot.custom_filters import StateFilter

from storages.sync_storages import Storage

from bot.logger import Logger
from bot.config import Config


def add_custom_filters(bot: TeleBot, cfg: Config, storage: Storage, logger: Logger):
    bot.add_custom_filter(StateFilter(bot))


__all__ = (
    "add_custom_filters",
)
