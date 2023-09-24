from aiogram import types
from aiogram.types import ChatActions, ReplyKeyboardMarkup, InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton

from filters import *
from keyboards.default.cb import blogersha_cb
from keyboards.default.markups import blogershi, questions, add_product, delete_product
from keyboards.inline.categories import get_markup_all_products
from loader import bot, dp, db


@dp.message_handler(IsAdmin(), commands='menu')
@dp.message_handler(IsAdmin(), text=blogershi)
async def admin_menu(message: types.Message):
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)

    await message.answer('CСамые лучшие блогерши только у нас!\n'
                         'ДАДА это всё ПРАВДА!!!!\n'
                         'ДАДА это всё ПРАВДА!!!!\n'
                         'ДАДА это всё ПРАВДА!!!!\n'
                         'ДАДА это всё ПРАВДА!!!!\n'
                         'блаблаблшаблабла\n', reply_markup=get_markup_all_products())

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(add_product, callback_data=add_product))
    await message.answer('Хотите что-нибудь добавить?', reply_markup=markup)



@dp.callback_query_handler(IsAdmin(), blogersha_cb.filter(action='get_body'))
async def get_body_blogershi(query: CallbackQuery, callback_data: dict):
    await query.message.delete()
    product_idx = callback_data['id']
    blog = db.fetchone('SELECT * FROM blogersha WHERE idx=?', (product_idx,))
    idx, title, body, price_trial, price_one_month, price_three_month, price_twelve_month, price_infinity_month = blog

    markup = InlineKeyboardMarkup(resize_keyboard=True, selective=True, row_width=1)

    markup.add(InlineKeyboardButton(price_trial, callback_data=blogersha_cb.new(id=idx, action='payment', price=price_trial)))
    markup.add(InlineKeyboardButton(price_one_month, callback_data=blogersha_cb.new(id=idx, action='payment', price=price_one_month)))
    markup.add(InlineKeyboardButton(price_three_month, callback_data=blogersha_cb.new(id=idx, action='payment', price=price_three_month)))
    markup.add(InlineKeyboardButton(price_twelve_month, callback_data=blogersha_cb.new(id=idx, action='payment', price=price_twelve_month)))
    markup.add(InlineKeyboardButton(price_infinity_month, callback_data=blogersha_cb.new(id=idx, action='payment', price=price_infinity_month)))
    markup.add(InlineKeyboardButton(delete_product, callback_data=blogersha_cb.new(id=idx, action='delete', price=price_one_month)))

    await query.message.answer(f"Название: {title}\n\n"
                               f"Описание: {body}\n\n", reply_markup=markup)


@dp.callback_query_handler(IsAdmin(), blogersha_cb.filter(action='delete'))
async def delete_product_callback_handler(query: CallbackQuery, callback_data: dict):
    product_idx = callback_data['id']
    db.query('DELETE FROM blogersha WHERE idx=?', (product_idx,))
    await query.answer('Удалено!')
    await query.message.delete()