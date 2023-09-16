import logging

from telebot.handler_backends import BaseMiddleware

from ...config.models import MessagesConfig, ButtonsConfig


class ExtraArgumentsMiddleware(BaseMiddleware):
    def __init__(
            self,
            messages: MessagesConfig,
            buttons: ButtonsConfig,
            logger: logging.Logger,
            page_size: int):
        super().__init__()
        self.messages = messages
        self.buttons = buttons
        self.logger = logger
        self.page_size = page_size
        self.update_types = ['message', 'callback_query']

    # argument naming is kept from the base class to avoid possible errors if passed as kwargs
    def pre_process(self, message, data: dict):
        # passing extra arguments to handlers
        data['messages'] = self.messages
        data['buttons'] = self.buttons
        data['logger'] = self.logger
        data['page_size'] = self.page_size

    # argument naming is kept from the base class to avoid possible errors if passed as kwargs
    def post_process(self, message, data: dict, exception: BaseException):
        pass
