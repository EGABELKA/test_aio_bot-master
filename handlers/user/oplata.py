from aiogram import types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from data import payment
from handlers.admin.add import blogersha_cb
from keyboards.default.markups import trial, one_month, three_month, twelve_month, infinity_month
from loader import db, dp, bot
from urllib.parse import urlencode

@dp.callback_query_handler(blogersha_cb.filter(action='payment'))
async def oplata(query: CallbackQuery, callback_data: dict):
    await query.message.delete()
    product_idx = callback_data['id']
    price = int(callback_data['price'])
    blog = db.fetchone('SELECT * FROM blogersha WHERE idx=?', (product_idx,))

    idx, title, body, price_trial, price_one_month, price_three_month, price_twelve_month, price_infinity_month = blog

    if price == price_trial:
        duration = trial
    elif price == price_one_month:
        duration = one_month
    elif price == price_three_month:
        duration = three_month
    elif price == price_twelve_month:
        duration = twelve_month
    else:
        duration = infinity_month

    product = payment.get_new_blog(price, id, body, duration)

    markupSecond = InlineKeyboardMarkup(row_width=1)
    getLinkToPay = types.InlineKeyboardButton(text="Получить ссылку для оплаты💳",
                                              url="https://aaio.io/merchant/pay?" + urlencode(product.params))
    IPayed = types.InlineKeyboardButton(text="Я оплатил☑️", callback_data="paying")
    backToList = types.InlineKeyboardButton(text="Назад⛔", callback_data="back_to_menu")
    markupSecond.add(getLinkToPay, IPayed, backToList)

    #bot.delete_message(query.message.chat.id, query.message.message_id)

    await query.message.answer(f"✅Сумма к оплате - {product.amount}р.\n"
                                      f"✅Срок подписки - {product.duration}\n"
                                      f"✅Описание подписки - {product.desc}\n\n"
                                      f"🔥Если всё верно, жми на кнопку \"Получить ссылку для оплаты\"\n\n"
                                      "🔎После оплаты, следует нажать на кнопку <Я оплатил☑️>\n\n"
                                      "❓Остались вопросы? Можешь обратиться в тех поддержку, написав комманду /sos, либо можешь написать ему в личку - [@nikita_imbochka]\n",
                               reply_markup=markupSecond, parse_mode='Markdown')
