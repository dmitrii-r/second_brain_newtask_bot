import os

from aiogram import types
from aiogram.filters import BaseFilter
from dotenv import load_dotenv

load_dotenv()

auth_ids: list[int] = list(map(int, os.getenv("AUTH_IDS").split()))


class AuthFilter(BaseFilter):
    async def __call__(self, event: types.TelegramObject) -> bool:
        return event.chat.id in auth_ids
