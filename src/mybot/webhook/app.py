from logging import Logger
from typing import Optional

from telebot import TeleBot


class Context:
    def __init__(self,
                 bot: Optional[TeleBot] = None,
                 secret_token: Optional[str] = None,
                 logger: Optional[Logger] = None):
        self.bot = bot
        self.secret_token = secret_token
        self.logger = logger


# TODO: Derive this class from your web framework's Application class
class Application:
    def __init__(self, *args, ctx: Optional[Context] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx or Context()
