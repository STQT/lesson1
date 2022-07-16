from pprint import pprint
from utils import getter, get_nationalize  # 3

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5476791595:AAEX6VPTeLqbl74sLp07B9E7Zvx1B4mBPJg'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    print(message)
    await message.answer("Привет я новый бот")


@dp.message_handler()
async def some_handler(message: types.Message):
    # x = getter()['title']

    # await message.answer(x)
    # print(type(getter()))
    name = await message.answer(get_nationalize(message.text))
    print(name)

executor.start_polling(dp, skip_updates=True)
