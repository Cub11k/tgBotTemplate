from telebot.storage import StateMemoryStorage, StateRedisStorage

from ...config.models import BotStateStorageConfig


# Pickle storage is intentionally left out
def setup_state_storage(storage_config: BotStateStorageConfig):
    if storage_config.type == 'memory':
        state_storage = StateMemoryStorage()
    else:
        state_storage = StateRedisStorage(
            host=storage_config.redis.host,
            port=storage_config.redis.port,
            db=storage_config.redis.db,
            password=storage_config.redis.password,
            prefix=storage_config.redis.prefix,
        )

    return state_storage
