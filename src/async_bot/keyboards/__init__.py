from collections import namedtuple

from async_bot.config import Buttons

from async_bot.keyboards.reply import ReplyKeyboards
from async_bot.keyboards.inline import InlineKeyboards


Keyboards = namedtuple("Keyboards", ["reply", "inline"])


def create_keyboards(keyboards: Buttons) -> Keyboards:
    return Keyboards(ReplyKeyboards(keyboards.reply), InlineKeyboards(keyboards.inline))


__all__ = (
   "Keyboards", "create_keyboards"
)
