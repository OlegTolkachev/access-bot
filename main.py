import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram import F

from aiogram import Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.markdown import hlink
import asyncio

TOKEN = os.getenv("BOT_TOKEN")  # Токен задается через Render
GROUP_ID = os.getenv("GROUP_ID")  # ID группы, например: "-1001234567890"
CHANNEL_ID = os.getenv("CHANNEL_ID")  # ID канала, например: "-1009876543210"

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)


@router.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id

    # Проверка подписки на канал
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status not in ["member", "administrator", "creator"]:
            raise Exception("Not subscribed")
    except:
        await message.answer("Пожалуйста, подпишитесь на канал и попробуйте снова.")
        return

    # Если подписка есть — приглашаем в группу
    invite_link = await bot.create_chat_invite_link(chat_id=GROUP_ID, name="Auto link", creates_join_request=False)
    await message.answer(f"Вы подписаны! Вот ваша ссылка на группу:\n{invite_link.invite_link}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
