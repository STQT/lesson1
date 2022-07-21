from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

TOKEN = "5446129541:AAEqHHFl3Qqp5EUXdE7F43gyphQorzrX3xo"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

group_id = -706230302


class Reg(StatesGroup):
    name = State()
    surname = State()
    phone = State()


class Complaints(StatesGroup):
    text = State()


@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    row_btns1 = [
        types.InlineKeyboardButton('О боте', callback_data='about'),
        types.InlineKeyboardButton('Регистрация', callback_data='registration')
    ]
    row_btns3 = [
        types.InlineKeyboardButton('Оставить жалобу', callback_data='affirm'),
    ]
    keyboard.row(*row_btns1)
    keyboard.row(*row_btns3)
    await msg.answer('Уже работает', reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data == 'about')
async def about_func(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer('Наша фирма занимается *работой*', parse_mode='MarkdownV2')


@dp.callback_query_handler(lambda call: call.data == 'registration')
async def registration_func(callback: types.CallbackQuery):
    print("@@@@@@@@@@@@@@@@@@")
    await callback.message.answer('Напишите своё имя')
    await Reg.name.set()


@dp.message_handler(state=Reg.name)
async def get_name(msg: types.Message, state: FSMContext):
    print("#################")
    async with state.proxy() as data:
        data['imya'] = msg.text
    await msg.answer("Теперь напиши мне фамилию")
    await Reg.surname.set()


@dp.message_handler(state=Reg.surname)
async def get_surname(msg: types.Message, state: FSMContext):
    print("%%%%%%%%%%%%%%%%%")
    async with state.proxy() as data:
        data['familiya'] = msg.text
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить телефон",
                                        request_contact=True)
    keyboard.add(button_phone)
    await msg.answer("Отправь телефон", reply_markup=keyboard)
    await Reg.phone.set()


@dp.message_handler(state=Reg.phone, content_types=['contact'])
async def get_phone(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = msg.contact.phone_number
        await msg.answer("Успешно зарегистрированы")

        await bot.send_message(group_id, "Имя: {}\n"
                                         "Фамилия: {}\n"
                                         "Телефон: {}\n".format(data.get('imya'),
                                                                data.get('familiya'),
                                                                data.get('phone')))
    await state.finish()


@dp.callback_query_handler(lambda call: call.data == 'affirm')
async def affirm_func(callback: types.CallbackQuery):
    await callback.message.answer('Оставьте свою жалобу')
    await Complaints.text.set()


@dp.message_handler(state=Complaints.text)
async def jaloba(msg: types.Message):
    await msg.forward(group_id)


@dp.message_handler(commands=['help'])
async def help(msg: types.Message):
    await msg.answer("Это помощь")


@dp.message_handler(lambda msg: msg.text == 'text')
async def foo_funct(msg: types.Message):
    await msg.answer(msg.text)


@dp.message_handler(lambda msg: msg.text == 'video')
async def foo_funct(msg: types.Message):
    # with open('videoplayback.mp4', 'rb') as f:
    #     x = await msg.answer_video(f)
    #     print(x)
    await msg.answer_video('BAACAgIAAxkDAAMPYtlvEq_w8kA_i9HVOCJdgGScr5sAAgUaAAJJlNBKd7RG9bUuz00pBA')


@dp.message_handler()
async def echo(msg: types.Message):
    await bot.send_message(msg.reply_to_message.forward_from.id, msg.text)

executor.start_polling(dp, skip_updates=True)
