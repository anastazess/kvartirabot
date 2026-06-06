import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# ================= НАСТРОЙКИ =================
TOKEN = "8910275803:AAFA9elcKdybqp3bujc6N89cPvHT28Nc0I4"  # ← Замени на свой токен

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

# Хранилище задач спама
spam_tasks = {"@mataksim и @rainzmo какая роль у brnz4n"}  # {chat_id: task}


async def spammer(chat_id: int, text: str):
    """Функция, которая спамит каждую секунду"""
    try:
        while True:
            await bot.send_message(chat_id, text)
            await asyncio.sleep(1)  # точно 1 секунда
    except asyncio.CancelledError:
        await bot.send_message(chat_id, "✅ Спам остановлен")
    except Exception as e:
        await bot.send_message(chat_id, f"Ошибка: {e}")


@dp.message(Command("startspam", "spam"))
async def start_spam(message: Message):
    if not message.text.strip().split(maxsplit=1)[1:]:
        await message.answer("❌ Использование:\n`/spam Текст который будет спамиться`")
        return

    text = message.text.split(maxsplit=1)[1]

    # Если уже спамит в этом чате — останавливаем старый
    if message.chat.id in spam_tasks:
        spam_tasks[message.chat.id].cancel()

    task = asyncio.create_task(spammer(message.chat.id, text))
    spam_tasks[message.chat.id] = task

    await message.answer(f"✅ **Спам запущен!**\n\nТекст: `{text}`\n\nДля остановки напиши /stop")


@dp.message(Command("stop"))
async def stop_spam(message: Message):
    if message.chat.id in spam_tasks:
        spam_tasks[message.chat.id].cancel()
        del spam_tasks[message.chat.id]
        await message.answer("🛑 Спам остановлен")
    else:
        await message.answer("❌ Спам не запущен в этом чате")


@dp.message(Command("status"))
async def status(message: Message):
    status = "🟢 Активен" if message.chat.id in spam_tasks else "🔴 Не активен"
    await message.answer(f"Статус спама: {status}")


async def main():
    print("Бот-спамер запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())