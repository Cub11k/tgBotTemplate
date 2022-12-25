from enum import Enum
from typing import Optional

from telebot.asyncio_storage import StatePickleStorage, StateRedisStorage

from async_bot.states.user import UserStates
from async_bot.states.admin import AdminStates

redis_installed = True
try:
    import aioredis
except ModuleNotFoundError:
    try:
        from redis import asyncio as aioredis
    except ModuleNotFoundError:
        redis_installed = False


class StateStorageType(Enum):
    pickle = "pickle"
    redis = "redis"


async def load_state_storage(storage_type: StateStorageType, file_path: Optional[str] = None,
                             redis_url: Optional[str] = None):
    if storage_type == StateStorageType.pickle:
        return StatePickleStorage(file_path) if file_path is not None else StatePickleStorage("../.states/states.pkl")
    elif storage_type == StateStorageType.redis:
        if redis_url is not None:
            if not redis_installed:
                raise ModuleNotFoundError("AioRedis is not installed. Install it via 'pip install aioredis'")
            kwargs = aioredis.connection.parse_url(redis_url)
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
