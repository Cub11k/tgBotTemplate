from telebot import TeleBot

from storages.sync_storages import Storage

from bot.logger import Logger
from bot.config import Config, Messages
from bot.keyboards import Keyboards

from bot.handlers.admin import AdminHandlers


def register_handlers(bot: TeleBot, cfg: Config, storage: Storage, logger: Logger,
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
