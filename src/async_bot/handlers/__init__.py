from telebot.async_telebot import AsyncTeleBot

from storages.async_storages import Storage

from logger import Logger

from async_bot.config import Config, Messages
from async_bot.keyboards import Keyboards

from async_bot.handlers.admin import AdminHandlers


def register_handlers(bot: AsyncTeleBot, cfg: Config, storage: Storage, logger: Logger,
                      messages: Messages, keyboards: Keyboards):
    kwargs = {
        "bot": bot,
        "cfg": cfg,
        "storage": storage,
        "logger": logger,
        "messages": messages,
        "keyboards": keyboards
    }
    admin_kwargs = kwargs
    AdminHandlers(**admin_kwargs).register()


__all__ = (
    "register_handlers",
)
