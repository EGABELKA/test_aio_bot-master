from aiogram.dispatcher.filters.state import StatesGroup, State

class SendChequeState(StatesGroup):
    photo = State()