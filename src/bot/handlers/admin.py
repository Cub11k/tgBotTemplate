from typing import Callable

from telebot import TeleBot
from telebot.types import Message
from telebot.apihelper import ApiException

from storages.sync_storages import Storage

from bot.logger import Logger
from bot.config import Config, Messages
from bot.keyboards import Keyboards

from bot.handlers.base_handlers import BaseHandlers


def get_args(text: str, required_args_num: int, max_args_num: int, args_filter: Callable):
    args = text.split(maxsplit=max_args_num)
    if len(args) < required_args_num + 1 or not args_filter(args[1:]):
        raise ValueError
    return args[1:]


class AdminHandlers(BaseHandlers):
    def __init__(self, bot: TeleBot, cfg: Config, storage: Storage, logger: Logger,
                 messages: Messages, keyboards: Keyboards):
        super().__init__()
        self.bot = bot
        self.cfg = cfg
        self.storage = storage
        self.logger = logger
        self.messages = messages
        self.keyboards = keyboards

    def register(self):
        self.bot.register_message_handler(self.ban, commands=["ban"],
                                          func=lambda msg: self._is_admin(msg.from_user.id))
        self.bot.register_message_handler(self.unban, commands=["unban"],
                                          func=lambda msg: self._is_admin(msg.from_user.id))

    def ban(self, msg: Message):
        try:
            args = get_args(msg.text, 1, 2, lambda lst: lst[0].isdecimal())
        except ValueError:
            self.bot.send_message(msg.chat.id, self.messages.help.ban)
            return
        user_id = int(args[0])
        if self._is_admin(user_id):
            self.bot.send_message(msg.chat.id, self.messages.admin.cant_ban_admin)
            return
        try:
            result = self.storage.get_data("banned_users")
            banned_users = result[0]
        except KeyError:
            self.storage.set_data(banned_users=[user_id])
        else:
            if not isinstance(banned_users, list):
                self.bot.send_message(msg.chat.id, f"{self.messages.admin.storage_corrupted} - banned_users")
                self.logger.storage_corrupted("banned_users")
                return
            else:
                if user_id in banned_users:
                    self.bot.send_message(msg.chat.id, self.messages.admin.already_banned)
                    return
                else:
                    banned_users.append(user_id)
                    self.storage.set_data(banned_users=banned_users)
                    self.logger.banned(user_id)
        finally:
            self.bot.send_message(msg.chat.id, self.messages.user.success)
            ban_reason = args[1] if len(args) == 2 else self.messages.user.ban_default_reason
            try:
                self.bot.send_message(user_id, f"{self.messages.user.banned} - {ban_reason}")
            except ApiException:
                self.logger.send_message_failed(user_id)
                pass

    def unban(self, msg: Message):
        try:
            args = get_args(msg.text, 1, 2, lambda lst: lst[0].isdecimal())
        except ValueError:
            self.bot.send_message(msg.chat.id, self.messages.help.unban)
            return
        user_id = int(args[0])
        try:
            result = self.storage.get_data("banned_users")
            banned_users = result[0]
        except KeyError:
            self.bot.send_message(msg.chat.id, self.messages.admin.not_banned)
        else:
            if not isinstance(banned_users, list):
                self.bot.send_message(msg.chat.id, f"{self.messages.admin.storage_corrupted} - banned_users")
                self.logger.storage_corrupted("banned_users")
                return
            else:
                if user_id not in banned_users:
                    self.bot.send_message(msg.chat.id, self.messages.admin.not_banned)
                    return
                else:
                    banned_users.remove(user_id)
                    self.storage.set_data(banned_users=banned_users)
                    self.logger.unbanned(user_id)
            self.bot.send_message(msg.chat.id, self.messages.user.success)
            try:
                self.bot.send_message(user_id, self.messages.user.unbanned)
            except ApiException:
                self.logger.send_message_failed(user_id)
                pass

    def _is_admin(self, user_id: int):
        return self.cfg.tg_bot.admin_id == user_id
