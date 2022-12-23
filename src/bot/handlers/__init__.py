from telebot import TeleBot

from storages import Storage

from bot.config import Config
from bot.logger import Logger

from bot.handlers.admin import AdminHandlers


def register_handlers(bot: TeleBot, cfg: Config, storage: Storage, logger: Logger):
    AdminHandlers(bot, cfg, storage, logger).register()


__all__ = (
    "register_handlers",
)
