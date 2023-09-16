import logging

from telebot import TeleBot

from ...config.models import MessagesConfig, ButtonsConfig

from .message_antiflood import MessageAntiFloodMiddleware
from .callback_query_antiflood import CallbackQueryAntiFloodMiddleware
from .extra_arguments import ExtraArgumentsMiddleware


def setup_middlewares(
        bot: TeleBot,
        timeout_message: str,
        timeout: float,
        messages: MessagesConfig,
        buttons: ButtonsConfig,
        logger: logging.Logger,
        page_size: int):
    # TODO: setup all middlewares here
    bot.setup_middleware(MessageAntiFloodMiddleware(bot, timeout_message, timeout))
    bot.setup_middleware(CallbackQueryAntiFloodMiddleware(bot, timeout_message, timeout))
    bot.setup_middleware(ExtraArgumentsMiddleware(messages, buttons, logger, page_size))
    pass
