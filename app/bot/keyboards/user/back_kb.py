from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def back_kb(to: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=f"{to}"
                )
            ]
        ]
    )
