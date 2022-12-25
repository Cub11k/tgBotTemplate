from typing import Optional
from dataclasses import dataclass

from storages import StorageType

from bot.states import StateStorageType


@dataclass
class Webhook:
    url: str
    certificate: Optional[str]
    private_key: Optional[str]
    secret_token: Optional[str]


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
    num_threads: int
    use_middlewares: bool
    state_storage: StateStorage
    log_file_path: Optional[str]
    webhook: Optional[Webhook]


@dataclass
class Storage:
    type: StorageType
    file_path: Optional[str]
    redis_url: Optional[str]
    redis_data_key: Optional[str]


@dataclass
class Config:
    tg_bot: TgBot
    storage: Storage
    messages_path: Optional[str]
    keyboards_path: Optional[str]


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
class ReplyButtons:
    pass


@dataclass
class InlineButtons:
    pass


@dataclass
class Buttons:
    reply: ReplyButtons
    inline: InlineButtons
