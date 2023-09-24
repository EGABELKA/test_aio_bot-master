from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

back_message = '👈 Назад'
confirm_message = '✅ Подтвердить заказ'
all_right_message = '✅ Все верно'
cancel_message = '🚫 Отменить'
menu_message = '📕 Меню'
my_account_message = '📝 Мой Аккаунт'
questions_adm = '👋 Вопросы'

catalog = '🛍️ Каталог'
cart = '🛒 Корзина'
delivery_status = '🚚 Статус заказа'

settings = '⚙️ Настройка каталога'
orders = '🚚 Заказы'
questions = '❓ Тех Поддержка'
write_message_user = '📧 Написать Человеку'

delete_product = '🗑️ Удалить Блогершу'
add_product = '➕ Добавить Блогершу'

blogershi = '🔥 Блогерши'

trial = '🔥ПРОБНИК🔥'
one_month = '🔥1 МЕСЯЦ🔥'
three_month = '🔥3 МЕСЯЦА🔥'
twelve_month = '🔥12 МЕСЯЦЕВ🔥'
infinity_month = '🔥НАВСЕГДА🔥'


def confirm_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(confirm_message)
    markup.add(back_message)

    return markup


def back_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(back_message)

    return markup


def check_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(back_message, all_right_message)

    return markup



def submit_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(cancel_message, all_right_message)

    return markup

def user_menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(blogershi, questions)
    return markup

def admin_menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(blogershi)
    markup.row(questions_adm, write_message_user)
    return markup