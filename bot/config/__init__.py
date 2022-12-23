import configparser

from bot.states import StateStorageType
from bot.storages import StorageType

from bot.config.models import Config
from bot.config.models import StateStorage, TgBot
from bot.config.models import Storage
from bot.config.models import HelpMessages, UserMessages, AdminMessages, Messages
from bot.config.models import UserButtons, AdminButtons, Buttons


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")

    tg_bot = config["tg_bot"]
    state_storage = config["state_storage"]

    storage = config["storage"]

    help_messages = config["help_messages"]
    user_messages = config["user_messages"]
    admin_messages = config["admin_messages"]

    user_buttons = config["user_buttons"]
    admin_buttons = config["admin_buttons"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot.get("token"),
            admin_id=tg_bot.getint("admin_id"),
            use_polling=tg_bot.getboolean("use_polling"),
            num_threads=tg_bot.getint("num_threads"),
            use_middlewares=tg_bot.getboolean("use_middlewares"),
            log_file_path=tg_bot.get("log_file_path"),
            state_storage=StateStorage(
                type=StateStorageType(state_storage.get("type")),
                file_path=state_storage.get("file_path"),
                redis_url=state_storage.get("redis_url")
            )
        ),
        storage=Storage(
            type=StorageType(storage.get("type")),
            file_path=storage.get("file_path"),
            redis_url=storage.get("redis_url")
        ),
        messages=Messages(
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
        ),
        buttons=Buttons(
            user=UserButtons(
            ),
            admin=AdminButtons(
            )
        )
    )


__all__ = (
    "Config",
    "load_config",
)
