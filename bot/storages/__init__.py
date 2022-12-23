from enum import Enum
from typing import Optional, Union

from bot.storages.base_storage import BaseStorage
from bot.storages.pickle_storage import PickleStorage
from bot.storages.json_storage import JSONStorage
from bot.storages.redis_storage import RedisStorage


class StorageType(Enum):
    pickle = "pickle"
    json = "json"
    redis = "redis"


def load_storage(storage_type: StorageType, file_path: Optional[str] = None, redis_url: Optional[str] = None):
    storage = {
        StorageType.pickle: PickleStorage,
        StorageType.json: JSONStorage,
        StorageType.redis: RedisStorage,
    }
    if storage_type in [StorageType.pickle, StorageType.json]:
        return storage[storage_type](file_path)
    elif storage_type == StorageType.redis:
        return storage[storage_type](redis_url)


Storage = Union[PickleStorage, JSONStorage, RedisStorage]
__all__ = (
    "Storage",
    "PickleStorage",
    "JSONStorage",
    "RedisStorage",
    "StorageType",
    "load_storage",
)
