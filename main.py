from pprint import pprint
from utils import getter, get_nationalize  # 3
from aiogram.utils.executor import start_webhook
from config import *
from aiogram import Bot, Dispatcher, executor, types

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    print(message)
    await message.answer("Привет я новый бот")


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    print("Bot started")


async def on_shutdown(dp):
    print("Bot stopped")
    print("ETO DEBUG", DEBUG)
    await bot.delete_webhook()


@dp.message_handler()
async def some_handler(message: types.Message):
    name = await message.answer(get_nationalize(message.text))
    print(name)


if __name__ == '__main__':
    if DEBUG:
        executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
    else:
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
