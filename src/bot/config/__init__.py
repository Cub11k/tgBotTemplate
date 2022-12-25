import os
import configparser

from storages import StorageType

from bot.states import StateStorageType

from bot.config.models import Config
from bot.config.models import Storage
from bot.config.models import StateStorage, Webhook, TgBot
from bot.config.models import HelpMessages, UserMessages, AdminMessages, Messages
from bot.config.models import ReplyButtons, InlineButtons, Buttons


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
            num_threads=tg_bot.getint("num_threads"),
            use_middlewares=tg_bot.getboolean("use_middlewares"),
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


def load_messages(path: str):
    messages = configparser.ConfigParser()
    messages.read(path, encoding="utf-8")

    help_messages = messages["help_messages"]
    user_messages = messages["user_messages"]
    admin_messages = messages["admin_messages"]

    return Messages(
        help=HelpMessages(
            ban=help_messages.get("ban"),
            unban=help_messages.get("unban")
        ),
        user=UserMessages(
            banned=user_messages.get("banned"),
            ban_default_reason=user_messages.get("ban_default_reason"),
            success=user_messages.get("success"),
            unbanned=user_messages.get("unbanned")
        ),
        admin=AdminMessages(
            already_banned=admin_messages.get("already_banned"),
            cant_ban_admin=admin_messages.get("cant_ban_admin"),
            not_banned=admin_messages.get("not_banned"),
            storage_corrupted=admin_messages.get("storage_corrupted")
        )
    )


def load_buttons(path: str):
    keyboards = configparser.ConfigParser()
    keyboards.read(path, encoding="utf-8")

    return Buttons(
        reply=ReplyButtons(
        ),
        inline=InlineButtons(
        )
    )


__all__ = (
    "Config", "load_config",
    "Messages", "load_messages",
    "ReplyButtons", "InlineButtons", "Buttons", "load_buttons",
)
