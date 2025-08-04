from aiogram import Bot, Dispatcher, executor, types
import os
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # @channelusername или -1001234567890
GROUP_ID = os.getenv("GROUP_ID")      # -1001234567890

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id

    # Проверка подписки
    member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
    if member.status not in ["creator", "administrator", "member"]:
        await message.reply("❌ Доступ запрещён. Подпишись на канал.")
        return

    # Генерация одноразовой ссылки
    invite_link = await bot.create_chat_invite_link(
        chat_id=GROUP_ID,
        member_limit=1,
        expire_date=int(asyncio.get_event_loop().time()) + 300  # 5 минут
    )

    await message.reply(f"✅ Вот твоя одноразовая ссылка:\n{invite_link.invite_link}")

if __name__ == "__main__":
    executor.start_polling(dp)
