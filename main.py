from pprint import pprint
from utils import getter, get_nationalize  # 3

from config import TOKEN, OWM_TOKEN
from aiogram import Bot, Dispatcher, executor, types


# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    print(message)
    await message.answer("Привет я новый бот")


@dp.message_handler()
async def some_handler(message: types.Message):
    name = await message.answer(get_nationalize(message.text))
    print(name)

executor.start_polling(dp, skip_updates=True)
