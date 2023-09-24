from aiogram.dispatcher.filters.state import StatesGroup, State

class WriteState(StatesGroup):
    cid = State()
    text = State()
    submit = State()