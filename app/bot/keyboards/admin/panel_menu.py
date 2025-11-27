from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.enums.order_status import OrderStatus
from config import Settings

def admin_main_menu_kb():
    kb = InlineKeyboardBuilder()

    kb.button(
        text="Управление заказами",
        callback_data="admin_orders_menu"
    )

    kb.button(
        text="Выгрузить все заказы в Excel",
        callback_data="admin_export_excel"
    )

    kb.adjust(1)
    return kb.as_markup()

def admin_orders_page_kb(orders, page: int, per_page: int = 8):
    kb = InlineKeyboardBuilder()

    start = page * per_page
    end = start + per_page
    page_orders = orders[start:end]

    for order in page_orders:
        kb.button(
            text=f"{Settings.human_status.get(order.status, order.status.value)} - №{order.id} - {order.name}",
            callback_data=f"admin_order_{order.id}"
        )

    kb.adjust(1)

    nav_row = []

    if page > 0:
        nav_row.append({
            "text": "⬅",
            "cb": f"admin_page_{page - 1}"
        })

    if end < len(orders):
        nav_row.append({
            "text": "➡",
            "cb": f"admin_page_{page + 1}"
        })

    for item in nav_row:
        kb.button(text=item["text"], callback_data=item["cb"])

    kb.button(
        text="Назад",
        callback_data="admin_panel"
    )

    kb.adjust(1)

    return kb.as_markup()


def admin_order_actions_kb(order_id: int):
    kb = InlineKeyboardBuilder()

    kb.button(
        text="Изменить статус",
        callback_data=f"admin_change_status_{order_id}"
    )

    kb.button(
        text="Назад",
        callback_data="admin_back_to_orders"
    )

    kb.adjust(1)

    return kb.as_markup()


def admin_status_select_kb(order_id: int):
    kb = InlineKeyboardBuilder()

    kb.button(
        text="🟡 Выполняется",
        callback_data=f"admin_set_status_{order_id}_{OrderStatus.processing.value}"
    )
    kb.button(
        text="🟢 Готово",
        callback_data=f"admin_set_status_{order_id}_{OrderStatus.done.value}"
    )
    kb.button(
        text="🔴 Закрыт",
        callback_data=f"admin_set_status_{order_id}_{OrderStatus.closed.value}"
    )

    kb.button(
        text="Назад",
        callback_data=f"admin_order_{order_id}"
    )

    kb.adjust(1)

    return kb.as_markup()


def admin_confirm_status_kb(order_id: int, new_status: str):
    kb = InlineKeyboardBuilder()

    kb.button(
        text="✅ Подтвердить",
        callback_data=f"admin_confirm_status_{order_id}_{new_status}"
    )
    kb.button(
        text="Отмена",
        callback_data=f"admin_order_{order_id}"
    )

    kb.adjust(1)
    return kb.as_markup()
