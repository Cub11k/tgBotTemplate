from typing import Optional
from dataclasses import dataclass

from config import Webhook, Storage

from async_bot.states import StateStorageType


@dataclass
class StateStorage:
    type: StateStorageType
    file_path: Optional[str]
    redis_url: Optional[str]


@dataclass
class TgBot:
    token: str
    admin_id: int
    use_polling: bool
    skip_pending: bool
    state_storage: StateStorage
    log_file_path: Optional[str]
    webhook: Optional[Webhook]


@dataclass
class Config:
    tg_bot: TgBot
    storage: Storage
    messages_path: Optional[str]
    keyboards_path: Optional[str]
