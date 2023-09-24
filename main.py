from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import executor
from logging import basicConfig, INFO

from filters import IsAdmin, IsUser
from keyboards.default.markups import user_menu_markup, admin_menu_markup
from loader import dp, db, bot
from data.config import ADMINS
import handlers

user_message = 'Пользователь'
admin_message = 'Админ'


@dp.message_handler(IsAdmin(), commands='start')
async def cmd_start_admin(message: types.Message):
    await message.answer('Ботик Админчика', reply_markup=admin_menu_markup())
    await handlers.admin.menu.admin_menu(message)

@dp.message_handler(IsUser(), commands='start')
async def cmd_start_admin(message: types.Message):
    await message.answer('@nyash_strimki', reply_markup=user_menu_markup())
    await handlers.user.menu.user_menu(message)

@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):
    cid = message.chat.id
    if cid not in ADMINS:
        ADMINS.append(cid)

    await message.answer('Включен админский режим.',
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):
    cid = message.chat.id
    if cid in ADMINS:
        ADMINS.remove(cid)

    await message.answer('Включен пользовательский режим.',
                         reply_markup=ReplyKeyboardRemove())


async def on_startup(dp):
    basicConfig(level=INFO)
    db.create_tables()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
