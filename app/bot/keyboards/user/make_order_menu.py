from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)

def cancel_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отменить", callback_data="cancel_order")]
    ])


def color_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬛ Черный", callback_data="color_Черный")
        ],
        [
            InlineKeyboardButton(text="⬜ Белый", callback_data="color_Белый")
        ],
        [
            InlineKeyboardButton(text="🟥 Красный", callback_data="color_Красный")
        ],
        [
            InlineKeyboardButton(text="🟦 Синий", callback_data="color_Синий")
        ],
        [
            InlineKeyboardButton(text="Свой цвет", callback_data="color_custom")
        ],
        [
            InlineKeyboardButton(text="Отменить", callback_data="cancel_order")
        ]
    ])


def material_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="PLA", callback_data="mat_PLA"),
        ],
        [
            InlineKeyboardButton(text="PETG", callback_data="mat_PETG"),
        ],
        [
            InlineKeyboardButton(text="ABS", callback_data="mat_ABS"),
        ],
        [
            InlineKeyboardButton(text="Отменить", callback_data="cancel_order")
            ]
    ])


def skip_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пропустить", callback_data="skip_notes")],
        [InlineKeyboardButton(text="Отменить", callback_data="cancel_order")]
    ])

def confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да, все верно", callback_data="confirm_yes")
        ],
        [
            InlineKeyboardButton(text="Нет, изменить", callback_data="confirm_no")
        ]
    ])

def my_orders_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Мои заказы", callback_data="my_orders")
        ]
    ])
