from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from app.services.order_service import OrderService
from app.services.user_service import UserService
from app.database.session import SessionLocal
from ...keyboards.user.back_kb import back_kb
from config import Settings

router = Router()
order_service = OrderService()


@router.callback_query(F.data == "my_orders")
async def my_orders_handler(callback: CallbackQuery):
    db = SessionLocal()

    user_service = UserService()
    user = user_service.repo.get_user_by_chat_id(db, callback.from_user.id)

    if not user:
        await callback.message.edit_text("Ошибка: пользователь не найден.")
        return

    orders = order_service.get_user_orders(db, user.id)
    db.close()

    if not orders:
        await callback.message.edit_text(
            "У вас пока нет заказов.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Назад", callback_data="main_menu")]
                ]
            )
        )
        return

    buttons = [
        [InlineKeyboardButton(
            text=f"{Settings.human_status.get(order.status, order.status.value)} / {order.name}",
            callback_data=f"order_{order.id}"
        )]
        for order in orders
    ]

    buttons.append([InlineKeyboardButton(text="Назад", callback_data="main_menu")])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(
        "Ваши заказы:",
        reply_markup=kb
    )


@router.callback_query(F.data.startswith("order_"))
async def order_details_handler(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[1])

    db = SessionLocal()
    order = order_service.get_order(db, order_id)
    db.close()

    if not order:
        await callback.message.edit_text("Ошибка: заказ не найден.")
        return

    human_status = Settings.human_status.get(order.status, order.status.value)

    

    text = (
        f"*Информация о заказе №{order.id}* ({order.name})\n\n"
        f"*Статус заказа:* {human_status}\n\n"
        f"*Пластик:* {order.material}\n"
        f"*Цвет:* {order.color}\n\n"
        f"**Кол-во моделей:** {order.quantity}\n"
        f"*Цена за 1 шт.:* {order.unit_price_rub} ₽\n"
        f"*Итого:* {order.price_rub} ₽\n\n"
        f"*Примечание:* {order.notes or '-'}\n"
    )

    queue = order_service.get_queue(db)
    pos = next((i+1 for i, o in enumerate(queue) if o.id == order.id), None)

    text += f"\n*Позиция в очереди:* {pos or '-'}"

    await callback.message.edit_text(
        text,
        reply_markup=back_kb("my_orders"),
        parse_mode="Markdown"
    )