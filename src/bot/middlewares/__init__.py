from telebot import TeleBot

from storages.sync_storages import Storage

from bot.logger import Logger
from bot.config import Config

from bot.middlewares.antiflood import MessageAntiFlood
from bot.middlewares.antiflood import CallbackAntiFlood
from bot.middlewares.ban_checker import BanChecker


def setup_middlewares(bot: TeleBot, cfg: Config, storage: Storage, logger: Logger):
    bot.setup_middleware(MessageAntiFlood(bot))
    bot.setup_middleware(CallbackAntiFlood(bot))
    bot.setup_middleware(BanChecker(storage))


__all__ = (
    "setup_middlewares",
)
