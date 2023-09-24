from aiogram import types
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, ChatActions

from keyboards.default.markups import blogershi, my_account_message, user_menu_markup
from keyboards.inline.categories import get_markup_all_products
from loader import dp
from loader import bot
from filters import IsAdmin, IsUser



@dp.message_handler(IsUser(), commands='menu')
@dp.message_handler(IsUser(), text=blogershi)
async def user_menu(message: Message):
    await message.answer('Самые лучшие блогерши только у нас!\n'
                         'ДАДА это всё ПРАВДА!!!!\n'
                         'ДАДА это всё ПРАВДА!!!!\n'
                         'ДАДА это всё ПРАВДА!!!!\n'
                         'ДАДА это всё ПРАВДА!!!!\n'
                         'блаблаблшаблабла\n', reply_markup=get_markup_all_products())


@dp.message_handler(IsUser(), text=my_account_message)
async def user_account(message: Message):
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)

    await message.answer('Вот типо ваш акк\n'
                         'Ваши подписки:\n'
                         'блаблаблшаблабла\n')



