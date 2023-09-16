import logging
import time
from typing import Optional

from telebot import TeleBot

from ..config.models import BotConfig, BotWebhookConfig, MessagesConfig, ButtonsConfig

from .filters import add_custom_filters
from .handlers import register_handlers
from .middlewares import setup_middlewares
from .states.storage import setup_state_storage


def launch_bot(bot: TeleBot,
               drop_pending: bool,
               use_webhook: bool,
               allowed_updates: Optional[list[str]] = None,
               webhook_config: Optional[BotWebhookConfig] = None
               ):
    if use_webhook:
        if webhook_config is None:
            raise ValueError('webhook_config is required if use_webhook is True')
        bot.remove_webhook()
        time.sleep(1)
        bot.set_webhook(
            url=f"{webhook_config.base_url}/{webhook_config.path}",
            certificate=webhook_config.cert_path,
            max_connections=webhook_config.max_connections,
            allowed_updates=allowed_updates,
            ip_address=webhook_config.ip_address,
            drop_pending_updates=drop_pending,
            secret_token=webhook_config.secret_token
        )
    else:
        bot.remove_webhook()
        time.sleep(1)
        bot.infinity_polling(allowed_updates=allowed_updates, skip_pending=drop_pending)


def stop_bot(bot: TeleBot, use_webhook: bool):
    if use_webhook:
        # be careful with this method when using webhook,
        # as the cleanup is usually meant to be called after the new version of the app was launched
        # and this bot.remove_webhook() will intervene with the new version of the app.
        # only remove webhook if you are sure that the new version of the app is not going to be launched
        # or isn't launched yet

        # bot.remove_webhook()
        pass
    else:
        bot.stop_polling()


def setup_bot(
        bot_config: BotConfig,
        messages: MessagesConfig,
        buttons: ButtonsConfig,
        logger: logging.Logger):
    state_storage = setup_state_storage(bot_config.state_storage)
    bot = TeleBot(bot_config.token, state_storage=state_storage, use_class_middlewares=bot_config.use_class_middlewares)

    add_custom_filters(bot, bot_config.owner_tg_id)
    if bot_config.use_class_middlewares:
        setup_middlewares(
            bot=bot,
            timeout_message=messages.anti_flood,
            timeout=bot_config.actions_timeout,
            messages=messages,
            buttons=buttons,
            logger=logger,
            page_size=bot_config.page_size
        )
    register_handlers(bot, buttons)

    return bot
