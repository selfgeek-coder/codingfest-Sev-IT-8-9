from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.enums.order_status import OrderStatus
from config import Settings


def admin_main_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Управление заказами", callback_data="admin_orders_menu"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Выгрузить все заказы в Excel", callback_data="admin_export_excel"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад", callback_data="main_menu"
                )
            ]
        ]
    )


def admin_orders_page_kb(orders, page: int, per_page: int = 8):
    start = page * per_page
    end = start + per_page
    page_orders = orders[start:end]

    kb = []

    for order in page_orders:
        kb.append([
            InlineKeyboardButton(
                text=f"{Settings.human_status.get(order.status, order.status.value)} - №{order.id} - {order.name}",
                callback_data=f"admin_order_{order.id}"
            )
        ])

    # Навигация
    nav_row = []
    if page > 0:
        nav_row.append(
            InlineKeyboardButton(text="⬅", callback_data=f"admin_page_{page - 1}")
        )
    if end < len(orders):
        nav_row.append(
            InlineKeyboardButton(text="➡", callback_data=f"admin_page_{page + 1}")
        )

    if nav_row:
        kb.append(nav_row)

    kb.append([
        InlineKeyboardButton(text="Назад", callback_data="admin_panel")
    ])

    return InlineKeyboardMarkup(inline_keyboard=kb)


def admin_order_actions_kb(order_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Поднять в очереди", callback_data=f"admin_q_up_{order_id}")],
            [InlineKeyboardButton(text="Опустить в очереди", callback_data=f"admin_q_down_{order_id}")],
            [InlineKeyboardButton(text="Изменить статус", callback_data=f"admin_change_status_{order_id}")],
            [InlineKeyboardButton(text="Назад", callback_data="admin_back_to_orders")],
        ]
    )


def admin_status_select_kb(order_id: int):
    allowed_statuses = [
        OrderStatus.processing,
        OrderStatus.done,
        OrderStatus.closed
    ]

    buttons = [
        [
            InlineKeyboardButton(
                text=Settings.human_status[status],
                callback_data=f"admin_set_status_{order_id}_{status.value}"
            )
        ]
        for status in allowed_statuses
    ]

    buttons.append([
        InlineKeyboardButton(
            text="Назад",
            callback_data=f"admin_order_{order_id}"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)



def admin_confirm_status_kb(order_id: int, new_status: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить",
                    callback_data=f"admin_confirm_status_{order_id}_{new_status}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data=f"admin_order_{order_id}"
                )
            ]
        ]
    )
