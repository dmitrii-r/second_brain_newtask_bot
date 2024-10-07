import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, BaseFilter
from dotenv import load_dotenv

from lexicon import greetings_text, unauthorized_text, input_text, error_text

load_dotenv()

BOT_TOKEN: str = os.getenv('BOT_TOKEN')
bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()

auth_ids: list[int] = list(map(int, os.getenv('AUTH_IDS').split()))


class AuthFilter(BaseFilter):
    async def __call__(self, event: types.TelegramObject) -> bool:
        return event.chat.id in auth_ids


@dp.message(CommandStart(), AuthFilter())
async def start(message: types.Message):
    await message.answer(
        greetings_text.format(message.from_user.first_name) + input_text
    )


@dp.message(AuthFilter())
async def process_get_message(message: types.Message):
    if message.text:
        await message.answer("отправлено")
    else:
        await message.answer(error_text + input_text)


@dp.message(CommandStart())
async def start_unauthorized(message: types.Message):
    await message.answer(unauthorized_text)


@dp.message()
async def process_unauthorized(message: types.Message):
    await message.answer(unauthorized_text)


if __name__ == '__main__':
    dp.run_polling(bot)
