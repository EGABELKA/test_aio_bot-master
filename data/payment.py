import hashlib

class get_new_blog():
    merchant_id = 'b3ba4134-6089-43bc-83a0-1fd7808c4b00'  # ID Вашего магазина
    currency = 'RUB'  # Валюта заказа
    secret = '8fe00602d5fa91c3e6d23b6255ce6e50'  # Секретный ключ №1
    lang = 'ru'  # Язык формы

    amount = 0  # Сумма к оплате
    order_id = ''  # Идентификатор заказа в Вашей системе
    desc = ''  # Описание заказа
    duration = ""  # Длительность подписки

    def __init__(self, amount, order_id, desc, duration):
        self.amount = amount
        self.order_id = order_id
        self.desc = desc
        self.duration = duration


    sign = f':'.join([
        str(merchant_id),
        str(amount),
        str(currency),
        str(secret),
        str(order_id)
    ])

    params = {
        'merchant_id': merchant_id,
        'amount': amount,
        'currency': currency,
        'order_id': order_id,
        'sign': hashlib.sha256(sign.encode('utf-8')).hexdigest(),
        'desc': desc,
        'lang': lang
    }