from aiogram import types

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery
from hashlib import md5
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.types.chat import ChatActions
from aiogram.types import ContentType

import handlers
from keyboards.default.cb import blogersha_cb
from keyboards.inline.categories import get_markup_all_products
from states import ProductState
from loader import dp, db
from filters import IsAdmin
from loader import bot
from keyboards.default.markups import *





# ------------------------------ Товары --------------------------------- #

# обработчик перехода к указанию названия товара
@dp.callback_query_handler(IsAdmin(), text=add_product)
async def process_add_product(query: CallbackQuery):
    await ProductState.title.set()

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(cancel_message)

    await query.message.answer('Название?', reply_markup=markup)

# обработчик отмены добавления товара
@dp.message_handler(IsAdmin(), text=cancel_message, state=ProductState.title)
async def process_cancel(message: Message, state: FSMContext):
    await message.answer('Ок, отменено!', reply_markup=ReplyKeyboardRemove())
    await state.finish()

    #await user_menu(message)

# обработчик перехода к указанию описания товара
@dp.message_handler(IsAdmin(), state=ProductState.title)
async def process_title(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text

    await ProductState.next()
    await message.answer('Описание?', reply_markup=back_markup())


# обработчик добавления в меню кнопки возврата
#def back_markup():
    #markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    #markup.add(back_message)

    #return markup

# обработчик возврата к добавлению товара
@dp.message_handler(IsAdmin(), text=back_message, state=ProductState.title)
async def process_title_back(message: Message, state: FSMContext):
    await process_add_product(message)

# обработчик возврата к изменению названия товара
@dp.message_handler(IsAdmin(), text=back_message, state=ProductState.body)
async def process_body_back(message: Message, state: FSMContext):
    await ProductState.title.set()

    async with state.proxy() as data:
        await message.answer(f"Изменить название с <b>{data['title']}</b>?",
                             reply_markup=back_markup())


# обработчик перехода к добавлению фото товара
@dp.message_handler(IsAdmin(), state=ProductState.body)
async def process_body(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['body'] = message.text

    await ProductState.next()
    await message.answer('Цена за пробный?', reply_markup=back_markup())




@dp.message_handler(IsAdmin(), state=ProductState.price_trial)
async def process_price_trial(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['price_trial'] = message.text

    await ProductState.next()
    await message.answer('Цена за месяц?', reply_markup=back_markup())


@dp.message_handler(IsAdmin(), state=ProductState.price_one_month)
async def process_price_one_month(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['price_one_month'] = message.text

    await ProductState.next()
    await message.answer('Цена за 3 месяца?', reply_markup=back_markup())


@dp.message_handler(IsAdmin(), state=ProductState.price_three_month)
async def process_price_three_month(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['price_three_month'] = message.text

    await ProductState.next()
    await message.answer('Цена за 12 месяцев?', reply_markup=back_markup())


@dp.message_handler(IsAdmin(), state=ProductState.price_twelve_month)
async def process_price_twelve_month(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['price_twelve_month'] = message.text

    await ProductState.next()
    await message.answer('Цена навсегда?', reply_markup=back_markup())

# обработчик формирования карточки товара после ввода цены
@dp.message_handler(IsAdmin(), lambda message: message.text.isdigit(),
                    state=ProductState.price_infinity_month)
async def process_price_infinity_month(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['price_infinity_month'] = message.text

        title = data['title']
        body = data['body']
        price_trial = data['price_trial']
        price_one_month = data['price_one_month']
        price_three_month = data['price_three_month']
        price_twelve_month = data['price_twelve_month']
        price_infinity_month = data['price_infinity_month']

        await ProductState.next()
        text = f'<b>{title}</b>\n\n{body}\n\nЦена: {price_one_month} рублей.'

        markup = check_markup()

        await message.answer(text, reply_markup=markup)


# функцию размещения клавиатуры с кнопками
# подтверждения и перехода на предыдущий шаг
#def check_markup():
    #markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    #markup.row(back_message, all_right_message)

    #return markup


# обработчик подтверждения регистрации товара
@dp.message_handler(IsAdmin(), text=all_right_message,
                    state=ProductState.confirm)
async def process_confirm(message: Message, state: FSMContext):
    async with state.proxy() as data:
        title = data['title']
        body = data['body']
        price_trial = data['price_trial']
        price_one_month = data['price_one_month']
        price_three_month = data['price_three_month']
        price_twelve_month = data['price_twelve_month']
        price_infinity_month = data['price_infinity_month']


        idx = md5(' '.join([title, body, price_one_month]
                           ).encode('utf-8')).hexdigest()

        db.query('INSERT INTO blogersha VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                 (idx, title, body, int(price_trial), int(price_one_month), int(price_three_month), int(price_twelve_month), int(price_infinity_month)))

    await state.finish()
    await message.answer('Готово!', reply_markup=ReplyKeyboardRemove())
    await handlers.admin.menu.admin_menu(message)



# обработчик возврата к редактированию цены
@dp.message_handler(IsAdmin(), text=back_message, state=ProductState.confirm)
async def process_confirm_back(message: Message, state: FSMContext):
    await ProductState.price_trial.set()

    async with state.proxy() as data:
        await message.answer(f"Изменить цену с <b>{data['price']}</b>?",
                             reply_markup=back_markup())


# обработчик возврата к редактированию
# описания и когда мы ввели текст вместо фото


# ------------------------------ валидаторы ---------------------------------#



# валидатор-обработчик если пользователь вместо подтверждения
# добавления товара в конце или отмены добавления напишет какой-то текст
@dp.message_handler(IsAdmin(),
                    lambda message: message.text not in [back_message,
                                                         all_right_message],
                    state=ProductState.confirm)
async def process_confirm_invalid(message: Message, state: FSMContext):
    await message.answer('Такого варианта не было.')
