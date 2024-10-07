from aiogram import types
from aiogram.filters import BaseFilter

from run_bot import auth_ids


class AuthFilter(BaseFilter):
    async def __call__(self, event: types.TelegramObject) -> bool:
        return event.chat.id in auth_ids
