from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Заказать", callback_data="make_order"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Мои заказы", callback_data="my_orders"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Корзина", callback_data="open_cart"
                )
            ]
        ]
    )
    return keyboard