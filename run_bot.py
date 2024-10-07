import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from filters import AuthFilter
from lexicon import (
    greetings_text,
    unauthorized_text,
    input_text,
    fault_text,
    error_text,
    success_text
)
from utils import create_note

load_dotenv()

logger = logging.getLogger(__name__)

BOT_TOKEN: str = os.getenv("BOT_TOKEN")
bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()

database_id: str = os.getenv("DATABASE_ID")
notion_token: str = os.getenv("NOTION_TOKEN")


@dp.message(CommandStart(), AuthFilter())
async def start(message: types.Message):
    await message.answer(
        greetings_text.format(message.from_user.first_name) + input_text
    )


@dp.message(AuthFilter())
async def process_get_message(message: types.Message):
    if message.text:
        answer = await create_note(database_id, notion_token, message.text)
        await message.answer([error_text, success_text][answer])
    else:
        await message.answer(fault_text + input_text)


@dp.message(CommandStart())
async def start_unauthorized(message: types.Message):
    await message.answer(unauthorized_text)


@dp.message()
async def process_unauthorized(message: types.Message):
    await message.answer(unauthorized_text)


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    dp.run_polling(bot)
