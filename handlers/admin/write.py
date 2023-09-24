from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from filters import IsAdmin
from keyboards.default.markups import write_message_user, submit_markup, all_right_message, cancel_message
from loader import dp, bot
from states import WriteState


@dp.message_handler(IsAdmin(), text=write_message_user)
async def write_message(message: types.Message):
    await message.answer('Введите id пользователя')
    await WriteState.cid.set()

@dp.message_handler(IsAdmin(),  state=WriteState.cid)
async def write_message(message: types.Message, state=WriteState.cid):
    async with state.proxy() as data:
        data['cid'] = message.text

    await WriteState.next()
    await message.answer('Введите текст для отправки')

@dp.message_handler(IsAdmin(),  state=WriteState.text)
async def write_message(message: types.Message, state=WriteState.cid):
    async with state.proxy() as data:
        data['text'] = message.text

    await WriteState.next()
    await message.answer('Убедитесь, что не ошиблись в ответе.',
                         reply_markup=submit_markup())

@dp.message_handler(IsAdmin(), text=all_right_message, state=WriteState.submit)
async def write_message(message: types.Message, state=WriteState.cid):
    async with state.proxy() as data:
        cid = data['cid']
        text = data['text']

        await bot.send_message(cid, f"Вам новое сообщение от администратора:\n\n"
                                    f"*{text}*", parse_mode="MarkdownV2")

    await state.finish()

@dp.message_handler(IsAdmin(), text=cancel_message)
async def process_send_answer(message: types.Message, state: FSMContext):
    await message.answer('Отменено!', reply_markup=ReplyKeyboardRemove())
    await state.finish()

