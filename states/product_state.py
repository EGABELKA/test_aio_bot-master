from aiogram.dispatcher.filters.state import StatesGroup, State


class CategoryState(StatesGroup):
    title = State()


class ProductState(StatesGroup):
    title = State()
    body = State()
    price_trial = State()
    price_one_month = State()
    price_three_month = State()
    price_twelve_month = State()
    price_infinity_month = State()
    confirm = State()
