import time

from telebot import TeleBot
from telebot.handler_backends import BaseMiddleware, CancelUpdate


class MessageAntiFlood(BaseMiddleware):
    def __init__(self, bot: TeleBot, timeout: float = 0.1):
        super().__init__()
        self.bot = bot
        self.timeout = timeout
        self.last_time = {}
        self.notified = {}

        self.update_types = ["message"]

    def pre_process(self, message, data):
        if message.from_user.id not in self.last_time:
            self.last_time[message.from_user.id] = message.date
            return
        if message.date - self.last_time[message.from_user.id] < self.timeout:
            if message.from_user.id not in self.notified or not self.notified[message.from_user.id]:
                self.notified[message.from_user.id] = True
                self.bot.send_message(message.chat.id, "Not so fast, bro, wait a sec!")
            return CancelUpdate()
        else:
            self.notified[message.from_user.id] = False
        self.last_time[message.from_user.id] = message.date

    def post_process(self, message, data, exception):
        pass


class CallbackAntiFlood(BaseMiddleware):
    def __init__(self, bot: TeleBot, timeout: float = 0.1):
        super().__init__()
        self.bot = bot
        self.timeout = timeout
        self.last_time = {}
        self.notified = {}

        self.update_types = ["callback_query"]

    def pre_process(self, callback, data):
        now = time.time()
        if callback.from_user.id not in self.last_time:
            self.last_time[callback.from_user.id] = now
            return
        if now - self.last_time[callback.from_user.id] < self.timeout:
            if callback.from_user.id not in self.notified or not self.notified[callback.from_user.id]:
                self.notified[callback.from_user.id] = True
                self.bot.answer_callback_query(callback.id, "Not so fast, bro, wait a sec!", show_alert=True)
            return CancelUpdate()
        else:
            self.notified[callback.from_user.id] = False
        self.last_time[callback.from_user.id] = now

    def post_process(self, callback, data, exception):
        pass
