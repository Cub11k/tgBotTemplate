import asyncio
from typing import Optional

from telebot.async_telebot import AsyncTeleBot

from storages.async_storages import load_storage

from logger import Logger

from async_bot.config import load_messages, load_buttons, load_config, Config
from async_bot.states import load_state_storage
from async_bot.filters import add_custom_filters
from async_bot.handlers import register_handlers
from async_bot.keyboards import create_keyboards, Keyboards
from async_bot.middlewares import setup_middlewares


async def init_bot(cfg: Config) -> AsyncTeleBot:
    state_storage = await load_state_storage(
        storage_type=cfg.tg_bot.state_storage.type,
        file_path=cfg.tg_bot.state_storage.file_path,
        redis_url=cfg.tg_bot.state_storage.redis_url
    )
    bot = AsyncTeleBot(
        token=cfg.tg_bot.token,
        state_storage=state_storage
    )

    messages = load_messages(cfg.messages_path if cfg.messages_path is not None else "../messages.ini")
    bot_keyboards = create_keyboards(
        load_buttons(cfg.keyboards_path if cfg.keyboards_path is not None else "../buttons.ini")
    )
    data_storage = await load_storage(
        storage_type=cfg.storage.type,
        file_path=cfg.storage.file_path,
        redis_url=cfg.storage.redis_url,
        redis_data_key=cfg.storage.redis_data_key
    )
    bot_logger = Logger()

    kwargs = {
        "bot": bot,
        "cfg": cfg,
        "storage": data_storage,
        "logger": bot_logger
    }
    custom_filters_kwargs = kwargs
    middlewares_kwargs = kwargs
    handlers_kwargs = {
        **kwargs,
        "messages": messages,
        "keyboards": bot_keyboards
    }
    add_custom_filters(**custom_filters_kwargs)
    setup_middlewares(**middlewares_kwargs)
    register_handlers(**handlers_kwargs)

    return bot


async def set_webhook(bot: AsyncTeleBot, cfg: Config):
    await bot.remove_webhook()
    await asyncio.sleep(1)
    await bot.set_webhook(
        url=cfg.tg_bot.webhook.url,
        certificate=cfg.tg_bot.webhook.certificate,
        secret_token=cfg.tg_bot.webhook.secret_token,
        drop_pending_updates=cfg.tg_bot.skip_pending
    )


async def launch(config_file_path: Optional[str] = None):
    cfg = load_config(path=config_file_path if config_file_path is not None else "../config.ini")
    bot = await init_bot(cfg)
    if cfg.tg_bot.use_polling:
        await bot.infinity_polling(skip_pending=cfg.tg_bot.skip_pending)
    else:
        await set_webhook(bot, cfg)


__all__ = (
    "launch",
)
