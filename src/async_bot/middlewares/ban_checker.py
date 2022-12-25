from telebot.asyncio_handler_backends import BaseMiddleware, CancelUpdate

from storages.async_storages import Storage


class BanChecker(BaseMiddleware):
    def __init__(self, storage: Storage):
        super().__init__()
        self.storage = storage

        self.update_types = ["message", "callback_query"]

    def pre_process(self, message, data):
        try:
            result = await self.storage.get_data("banned_users")
            banned_users = result[0]
        except KeyError:
            # no banned users
            pass
        else:
            if message.from_user.id in banned_users:
                return CancelUpdate()

    def post_process(self, message, data, exception):
        pass
