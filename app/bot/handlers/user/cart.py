from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message

from app.database.session import SessionLocal
from app.services.cart_service import CartService
from app.services.order_service import OrderService
from app.services.user_service import UserService
from ...keyboards.user.cart_menu import cart_actions_kb
from ...keyboards.user.back_kb import back_kb

from config import Settings

import time

router = Router()

cart_service = CartService()
user_service = UserService()
order_service = OrderService()


@router.callback_query(F.data == "open_cart")
async def open_cart(callback: CallbackQuery):
    db = SessionLocal()
    user = user_service.repo.get_user_by_chat_id(db, callback.from_user.id)
    items = cart_service.get_cart(db, user.id)

    if not items:
        return await callback.message.edit_text("На данный момент ваша корзина пуста :(\n\nОформите заказ и он попадет в корзину.",
                                                reply_markup=back_kb("main_menu"))

    text = "*Ваша корзина:*\n\n"

    for item in items:
        text += (
            f"🔹 Заказ *{item.name}* №{item.id}\n"
            f"Количество: {item.quantity}\n"
            f"Материал: {item.material}\n"
            f"Цена: {round(item.price_rub)} ₽\n"
        )

    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=cart_actions_kb()
    )
    await callback.answer()


@router.callback_query(F.data == "cart_clear")
async def cart_clear(callback: CallbackQuery):
    db = SessionLocal()

    user = user_service.repo.get_user_by_chat_id(db, callback.from_user.id)
    if not user:
        return await callback.message.edit_text("Ошибка: пользователь не найден")

    cart_service.clear_cart(db, user.id)

    await callback.answer("Корзина успешно очищена")


@router.callback_query(F.data == "cart_checkout")
async def checkout(callback: CallbackQuery, bot: Bot):
    db = SessionLocal()

    user = user_service.repo.get_user_by_chat_id(db, callback.from_user.id)
    if not user:
        return await callback.message.edit_text("Ошибка: пользователь не найден")

    cart = cart_service.get_cart(db, user.id)

    if not cart:
        return await callback.answer("Корзина пуста", show_alert=True)

    created_orders = []

    for item in cart:
        order = order_service.create_order(
            db=db,
            user_id=user.id,
            name=item.name,
            quantity=item.quantity,
            material=item.material,
            color=item.color,
            full_name=item.full_name,
            notes=item.notes,
            stl_path=item.stl_path,
            price_rub=item.price_rub,
            unit_price_rub=item.unit_price_rub
        )
        created_orders.append(order)

    cart_service.clear_cart(db, user.id)

    for order in created_orders:
        for admin_id in Settings.admins:
            try:
                await bot.send_message(admin_id, f"Поступил новый заказ №{order.id} - {order.name}.", parse_mode="Markdown")
            except Exception as e:
                print(f"Ошибка отправки админу {admin_id}: {e}")



    await callback.message.answer(
        "🎉"
    )

    time.sleep(0.5)

    await callback.message.answer(
        "Товары успешно оформлены."
    )

    await callback.answer()
