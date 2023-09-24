from aiogram import types

import handlers
from data.config import ADMINS
from filters import IsUser
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ContentType

from keyboards.default.markups import add_product, delete_product, trial, one_month, three_month, twelve_month, \
    infinity_month
from keyboards.inline.categories import get_markup_all_products, get_markup_to_menu
from aiogram.types import CallbackQuery
from aiogram.types.chat import ChatActions
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from keyboards.inline.categories import categories_markup
from loader import dp
from loader import db
from loader import bot
from keyboards.default.cb import blogersha_cb
from states.send_cheque_state import SendChequeState


@dp.callback_query_handler(IsUser(), blogersha_cb.filter(action='get_body'))
async def get_body_blogershi(query: CallbackQuery, callback_data: dict):
    await query.message.delete()
    product_idx = callback_data['id']
    blog = db.fetchone('SELECT * FROM blogersha WHERE idx=?', (product_idx,))
    idx, title, body, price_trial, price_one_month, price_three_month, price_twelve_month, price_infinity_month = blog

    markup = InlineKeyboardMarkup(resize_keyboard=True, selective=True, row_width=1)

    markup.add(InlineKeyboardButton(trial, callback_data=blogersha_cb.new(id=idx, action='payment', price=price_trial)))
    markup.add(InlineKeyboardButton(one_month, callback_data=blogersha_cb.new(id=idx, action='payment', price=price_one_month)))
    markup.add(InlineKeyboardButton(three_month, callback_data=blogersha_cb.new(id=idx, action='payment', price=price_three_month)))
    markup.add(InlineKeyboardButton(twelve_month, callback_data=blogersha_cb.new(id=idx, action='payment', price=price_twelve_month)))
    markup.add(InlineKeyboardButton(infinity_month, callback_data=blogersha_cb.new(id=idx, action='payment', price=price_infinity_month)))

    await query.message.answer(f"Название: {title}\n\n"
                               f"Описание: {body}\n\n", reply_markup=markup)

    #await query.message.delete()

@dp.callback_query_handler(IsUser(), text="paying")
async def callback_paying(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer('Теперь требуется отправить чек с оплатой!')
    await SendChequeState.photo.set()

@dp.message_handler(IsUser(), content_types=ContentType.PHOTO, state=SendChequeState.photo)
async def send_paying_to_admin(message: types.Message, state: FSMContext):
    fileID = message.photo[-1].file_id
    file_info = await bot.get_file(fileID)
    downloaded_file = (await bot.download_file(file_info.file_path)).read()
    cid = message.from_user.id
    await message.answer('Супер! теперь ждите крч около 24 часов мы вам отправим ссылку на канал с сливом', reply_markup=get_markup_to_menu())
    await bot.send_photo(ADMINS[0], downloaded_file, f'Пользователь: {cid}')

    await state.finish()

@dp.callback_query_handler(IsUser(), text='back_to_menu')
async def callback_back_to_menu(query: CallbackQuery):
    await query.message.delete()
    await handlers.user.menu.user_menu(query.message)

