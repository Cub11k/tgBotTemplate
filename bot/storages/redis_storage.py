import json
import atexit
from typing import Optional
from bot.storages.base_storage import BaseStorage

redis_installed = True
try:
    from redis import Redis, ConnectionPool
except ModuleNotFoundError:
    redis_installed = False


def create_connection_pool(redis_url):
    if not redis_installed:
        raise ModuleNotFoundError("Redis is not installed. Install it via 'pip install redis'")
    return ConnectionPool.from_url(redis_url)


class RedisStorage(BaseStorage):
    def __init__(self, redis_url: Optional[str]):
        super().__init__()
        self.redis = create_connection_pool(redis_url if redis_url is not None else "redis://localhost/")
        self.load()

        atexit.register(self.dump)

    def load(self):
        connection = Redis(connection_pool=self.redis)
        result = connection.get("data")
        connection.close()
        if result is not None:
            self.data = json.loads(result)

    def dump(self):
        connection = Redis(connection_pool=self.redis)
        connection.set("data", json.dumps(self.data))
        connection.close()
