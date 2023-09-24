from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

import handlers
from handlers.admin.add import blogersha_cb
from keyboards.default.markups import menu_message
from loader import db



def categories_markup():
    global category_cb

    markup = InlineKeyboardMarkup()
    for idx, title in db.fetchall('SELECT * FROM categories'):
        markup.add(InlineKeyboardButton(title,
                                        callback_data=category_cb.new(id=idx,
                                                                      action='view')))

    return markup


def get_markup_all_products():
    blogersha = db.fetchall('''SELECT * FROM blogersha product''')
    inline_markup = InlineKeyboardMarkup(resize_keyboard=True, selective=True, row_width=1)

    for idx, title, body, price_trial, price_one_month, price_three_month, price_twelve_month, price_infinity_month in blogersha:
        inline_markup.add(
            InlineKeyboardButton(title, callback_data=blogersha_cb.new(id=idx, action='get_body', price=price_trial)))

    return inline_markup

def get_markup_to_menu():
    inline_markup = InlineKeyboardMarkup()
    inline_markup.add(InlineKeyboardButton(menu_message, callback_data='back_to_menu'))
    return inline_markup

