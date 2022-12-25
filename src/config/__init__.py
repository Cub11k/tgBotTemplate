import configparser

from config.models import Webhook, Storage
from config.models import HelpMessages, UserMessages, AdminMessages, Messages
from config.models import ReplyButtons, InlineButtons, Buttons


def load_messages(path: str):
    messages = configparser.ConfigParser()
    messages.read(path, encoding="utf-8")

    help_messages = messages["help_messages"]
    user_messages = messages["user_messages"]
    admin_messages = messages["admin_messages"]

    return Messages(
        help=HelpMessages(
            ban=help_messages.get("ban"),
            unban=help_messages.get("unban")
        ),
        user=UserMessages(
            banned=user_messages.get("banned"),
            ban_default_reason=user_messages.get("ban_default_reason"),
            success=user_messages.get("success"),
            unbanned=user_messages.get("unbanned")
        ),
        admin=AdminMessages(
            already_banned=admin_messages.get("already_banned"),
            cant_ban_admin=admin_messages.get("cant_ban_admin"),
            not_banned=admin_messages.get("not_banned"),
            storage_corrupted=admin_messages.get("storage_corrupted")
        )
    )


def load_buttons(path: str):
    keyboards = configparser.ConfigParser()
    keyboards.read(path, encoding="utf-8")

    return Buttons(
        reply=ReplyButtons(
        ),
        inline=InlineButtons(
        )
    )


__all__ = (
    "Webhook", "Storage",
    "Messages", "load_messages",
    "ReplyButtons", "InlineButtons", "Buttons", "load_buttons",
)
