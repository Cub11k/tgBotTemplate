import time
from typing import Optional

from telebot import TeleBot

from bot.config import load_config, Config
from bot.states import load_state_storage
from bot.storages import load_storage
from bot.filters import add_custom_filters
from bot.handlers import register_handlers
from bot.middlewares import setup_middlewares
from bot.logger import Logger


def init_bot(cfg: Config) -> TeleBot:
    data_storage = load_storage(
        storage_type=cfg.storage.type,
        file_path=cfg.storage.file_path,
        redis_url=cfg.storage.redis_url
    )
    bot_logger = Logger()

    state_storage = load_state_storage(
        storage_type=cfg.tg_bot.state_storage.type,
        file_path=cfg.tg_bot.state_storage.file_path,
        redis_url=cfg.tg_bot.state_storage.redis_url
    )
    bot = TeleBot(
        token=cfg.tg_bot.token,
        num_threads=cfg.tg_bot.num_threads,
        use_class_middlewares=cfg.tg_bot.use_middlewares,
        state_storage=state_storage
    )

    kwargs = {
        "bot": bot,
        "cfg": cfg,
        "storage": data_storage,
        "logger": bot_logger
    }
    add_custom_filters(**kwargs)
    if cfg.tg_bot.use_middlewares:
        setup_middlewares(**kwargs)
    register_handlers(**kwargs)

    return bot


def set_webhook(bot: TeleBot, cfg: Config):
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(
        url=cfg.tg_bot.webhook.url,
        certificate=cfg.tg_bot.webhook.certificate,
        secret_token=cfg.tg_bot.webhook.secret_token,
        drop_pending_updates=cfg.tg_bot.skip_pending
    )


def launch(config_file_path: Optional[str] = None):
    cfg = load_config(path=config_file_path if config_file_path is not None else "../config.ini")
    bot = init_bot(cfg)
    if cfg.tg_bot.use_polling:
        bot.infinity_polling(skip_pending=cfg.tg_bot.skip_pending)
    else:
        set_webhook(bot, cfg)


__all__ = (
    "launch",
)
