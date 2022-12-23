from enum import Enum
from typing import Optional
from redis.connection import parse_url

from telebot.storage import StatePickleStorage, StateRedisStorage

from bot.states.user import UserStates
from bot.states.admin import AdminStates


class StateStorageType(Enum):
    pickle = "pickle"
    redis = "redis"


def load_state_storage(storage_type: StateStorageType, file_path: Optional[str] = None,
                       redis_url: Optional[str] = None):
    if storage_type == StateStorageType.pickle:
        return StatePickleStorage(file_path) if file_path is not None else StatePickleStorage("../.states/states.pkl")
    elif storage_type == StateStorageType.redis:
        if redis_url is not None:
            kwargs = parse_url(redis_url)
            return StateRedisStorage(
                kwargs["host"] if "host" in kwargs.keys() else "localhost",
                kwargs["port"] if "port" in kwargs.keys() else "6379",
                kwargs["db"] if "db" in kwargs.keys() else 0,
                kwargs["password"] if "password" in kwargs.keys() else None
            )
        else:
            return StateRedisStorage()


__all__ = (
    "AdminStates",
    "UserStates",
    "StateStorageType",
    "load_state_storage",
)
