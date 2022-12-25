import os
import configparser

from storages import StorageType

from config import Messages, load_messages
from config import ReplyButtons, InlineButtons, Buttons, load_buttons

from async_bot.states import StateStorageType

from async_bot.config.models import Config
from async_bot.config.models import Storage
from async_bot.config.models import StateStorage, Webhook, TgBot


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")

    tg_bot = config["tg_bot"]
    state_storage = config["state_storage"]
    webhook = config["webhook"] if not tg_bot.getboolean("use_polling") else None

    storage = config["storage"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot.get("token", vars=os.environ),
            admin_id=tg_bot.getint("admin_id"),
            use_polling=tg_bot.getboolean("use_polling"),
            skip_pending=tg_bot.getboolean("skip_pending"),
            state_storage=StateStorage(
                type=StateStorageType(state_storage.get("type")),
                file_path=state_storage.get("file_path", fallback=None),
                redis_url=state_storage.get("redis_url", fallback=None)
            ),
            log_file_path=tg_bot.get("log_file_path"),
            webhook=Webhook(
                url=webhook.get("url"),
                certificate=webhook.get("certificate", fallback=None),
                private_key=webhook.get("private_key", fallback=None, vars=os.environ),
                secret_token=webhook.get("secret_token", fallback=None, vars=os.environ)
            ) if webhook is not None else None
        ),
        storage=Storage(
            type=StorageType(storage.get("type")),
            file_path=storage.get("file_path", fallback=None),
            redis_url=storage.get("redis_url", fallback=None),
            redis_data_key=storage.get("redis_data_key", fallback=None)
        ),
        messages_path=config.get("messages", "path", fallback=None),
        keyboards_path=config.get("keyboards", "path", fallback=None)
    )


__all__ = (
    "Config", "load_config",
    "Messages", "load_messages",
    "ReplyButtons", "InlineButtons", "Buttons", "load_buttons",
)
