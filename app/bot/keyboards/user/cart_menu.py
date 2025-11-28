from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def cart_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Перейти в корзину",
                    callback_data="open_cart"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Добавить еще",
                    callback_data="make_order"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data="main_menu"
                )
            ]
        ]
    )


def cart_actions_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Оформить все товары",
                    callback_data="cart_checkout"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Очистить корзину",
                    callback_data="cart_clear"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data="main_menu"
                )
            ]
        ]
    )
