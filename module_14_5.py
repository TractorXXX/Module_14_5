from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext

import asyncio

from keyboards import *
from crud_functions import *
import texts

# api = '***' # Удалил реальный ключ, как было сказано в задании.
api = '7678291396:AAHLit59XAefhk7yGTYeT4jRoHPAbtQffDA'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(commands='start')
async def start(message):
    await message.answer(texts.welcome, reply_markup=start_kb)

# Модернизированная функция get_buying_list, где вместо обычной нумерации продуктов используем
# функцию get_all_products из crud_functions.

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    list_products = get_all_products()
    i = 0
    for product in list_products:
        i += 1
        with open(f'{i}.png', 'rb') as img:
            await message.answer(f'Название: {product[1]} | Описание: {product[2]} |'
                                 f' Цена: {product[3]}')
            await message.answer_photo(img)

    await message.answer(texts.choice_product, reply_markup=inline_menu)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(texts.buy_product)
    await call.answer()

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer(texts.info_bot)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer(texts.choice_option, reply_markup=kb_in)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(texts.formula)
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer(texts.age, reply_markup=start_kb)
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer(texts.growth, reply_markup=start_kb)
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer(texts.weight, reply_markup=start_kb)
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()

# Упрощённая формула Миффлина - Сан Жеора

    calculator_calories = 10 * int(data['third']) + 6.25 * int(data['second']) - 5 * int(data['first']) + 5
    await message.answer(f'Для похудения или сохранения нормального веса, '
                         f'Вам нужно потреблять не более {calculator_calories} калорий', reply_markup=start_kb)
    await state.finish()

# Машина состояний: цепочка изменений состояний RegistrationState.

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer(texts.registration)
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(username=message.text)
    if is_included(message.text):
        await message.answer(texts.again_registration)
        await RegistrationState.username.set()
    else:
        await message.answer(texts.user_email)
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer(texts.age)
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    user_name = data['username']
    await state.finish()
    await message.answer(f'Пользователь {user_name} добавлен.', reply_markup=start_kb)

# Следующий хендлер перехватывает все остальные сообщения

@dp.message_handler()
async def start(message):
    await message.answer(texts.start)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
