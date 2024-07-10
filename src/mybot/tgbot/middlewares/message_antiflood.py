from telebot import TeleBot
from telebot.types import Message
from telebot.handler_backends import BaseMiddleware, CancelUpdate


class MessageAntiFloodMiddleware(BaseMiddleware):
    def __init__(self, bot: TeleBot, timeout_message: str, timeout: float):
        super().__init__()
        self.bot = bot
        self.timeout_message = timeout_message
        self.timeout = timeout
        self.last_message = {}
        self.update_types = ['message']

    # argument naming is kept from the base class to avoid possible errors if passed as kwargs
    def pre_process(self, message: Message, data: dict):
        if message.from_user.id not in self.last_message:
            self.last_message[message.from_user.id] = message.date
            return
        if message.date - self.last_message[message.from_user.id] < self.timeout:
            self.last_message[message.from_user.id] = message.date
            self.bot.send_message(message.chat.id, self.timeout_message)
            return CancelUpdate()
        self.last_message[message.from_user.id] = message.date

    # argument naming is kept from the base class to avoid possible errors if passed as kwargs
    def post_process(self, message: Message, data: dict, exception: BaseException):
        pass
