from telebot.async_telebot import AsyncTeleBot

from storages.async_storages import Storage

from logger import Logger

from async_bot.config import Config

from async_bot.middlewares.antiflood import MessageAntiFlood
from async_bot.middlewares.antiflood import CallbackAntiFlood
from async_bot.middlewares.ban_checker import BanChecker


def setup_middlewares(bot: AsyncTeleBot, cfg: Config, storage: Storage, logger: Logger):
    bot.setup_middleware(MessageAntiFlood(bot))
    bot.setup_middleware(CallbackAntiFlood(bot))
    bot.setup_middleware(BanChecker(storage))


__all__ = (
    "setup_middlewares",
)
