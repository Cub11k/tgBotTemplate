from typing import Optional
from dataclasses import dataclass

from bot.states import StateStorageType
from bot.storages import StorageType


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
    num_threads: int
    use_middlewares: bool
    log_file_path: Optional[str]
    state_storage: StateStorage


@dataclass
class Storage:
    type: StorageType
    file_path: Optional[str]
    redis_url: Optional[str]


@dataclass
class HelpMessages:
    ban: str
    unban: str


@dataclass
class UserMessages:
    banned: str
    ban_default_reason: str
    success: str
    unbanned: str


@dataclass
class AdminMessages:
    already_banned: str
    cant_ban_admin: str
    not_banned: str
    storage_corrupted: str


@dataclass
class Messages:
    help: HelpMessages
    user: UserMessages
    admin: AdminMessages


@dataclass
class UserButtons:
    pass


@dataclass
class AdminButtons:
    pass


@dataclass
class Buttons:
    user: UserButtons
    admin: AdminButtons


@dataclass
class Config:
    tg_bot: TgBot
    storage: Storage
    messages: Messages
    buttons: Buttons
