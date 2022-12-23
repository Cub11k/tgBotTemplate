from typing import Optional

from telebot import TeleBot

from bot.config import load_config
from bot.states import load_state_storage
from bot.storages import load_storage
from bot.filters import add_filters
from bot.handlers import register_handlers
from bot.middlewares import setup_middlewares
from bot.logger import Logger


class YourBotName:
    def __init__(self, config_file_path: Optional[str] = None):
        self.cfg = load_config(path=config_file_path if config_file_path is not None else "../config.ini")

        data_storage = load_storage(
            storage_type=self.cfg.storage.type,
            file_path=self.cfg.storage.file_path,
            redis_url=self.cfg.storage.redis_url
        )
        bot_logger = Logger()

        state_storage = load_state_storage(
            storage_type=self.cfg.tg_bot.state_storage.type,
            file_path=self.cfg.tg_bot.state_storage.file_path,
            redis_url=self.cfg.tg_bot.state_storage.redis_url
        )
        self.bot = TeleBot(
            token=self.cfg.tg_bot.token,
            num_threads=self.cfg.tg_bot.num_threads,
            use_class_middlewares=self.cfg.tg_bot.use_middlewares,
            state_storage=state_storage
        )

        kwargs = {
            "bot": self.bot,
            "cfg": self.cfg,
            "storage": data_storage,
            "logger": bot_logger
        }
        add_filters(**kwargs)
        setup_middlewares(**kwargs)
        register_handlers(**kwargs)

    def set_webhook(self):
        pass

    def launch(self):
        if self.cfg.tg_bot.use_polling:
            self.bot.infinity_polling(skip_pending=True)
        else:
            self.set_webhook()


__all__ = (
    "YourBotName",
)
