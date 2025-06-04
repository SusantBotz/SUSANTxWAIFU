from pyrogram import filters
from pyrogram.types import Message

SUDO_USERS = (5536473064, 8019277081)

async def is_sudo(_, __, message: Message):
    return message.from_user and message.from_user.id in SUDO_USERS

sudo_filter = filters.create(is_sudo)
