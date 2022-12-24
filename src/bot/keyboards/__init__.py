from collections import namedtuple

from bot.config.models import Buttons

from bot.keyboards.reply import ReplyKeyboards
from bot.keyboards.inline import InlineKeyboards


Keyboards = namedtuple("Keyboards", ["reply", "inline"])


def create_keyboards(keyboards: Buttons) -> Keyboards:
    return Keyboards(ReplyKeyboards(keyboards.reply), InlineKeyboards(keyboards.inline))


__all__ = (
   "Keyboards", "create_keyboards"
)
