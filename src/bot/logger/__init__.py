import sys
import logging
from typing import Optional


class Logger:
    def __init__(self, file_path: Optional[str] = None):
        self.logger = logging.getLogger("Bot")
        formatter = logging.Formatter(
            '%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: "%(message)s"'
        )

        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(fmt=formatter)
        self.logger.addHandler(hdlr=sh)

        fh = logging.FileHandler(filename=file_path if file_path is not None else "../bot.log", encoding="utf-8")
        fh.setFormatter(fmt=formatter)
        self.logger.addHandler(hdlr=fh)

        self.logger.setLevel(level=logging.INFO)

    def banned(self, user_id: int):
        self.logger.info(f"User with tg_id {user_id} was banned")

    def send_message_failed(self, user_id: int):
        self.logger.info(f"Failed to send message to user with tg_id {user_id}")

    def storage_corrupted(self, msg):
        self.logger.error(f"Storage corrupted - {msg}!")

    def unbanned(self, user_id: int):
        self.logger.info(f"User with tg_id {user_id} was unbanned")


__all__ = (
    "Logger",
)
