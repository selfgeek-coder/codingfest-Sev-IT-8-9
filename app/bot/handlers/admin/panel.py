from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import app.excel
from app.services.user_service import UserService
from app.database.session import SessionLocal
from app.services.order_service import OrderService
from app.utils import is_admin
from app.enums.order_status import OrderStatus
from ...keyboards.admin.panel_menu import (
    admin_main_menu_kb,
    admin_orders_page_kb,
    admin_order_actions_kb,
    admin_status_select_kb,
    admin_confirm_status_kb,
)
from app.excel import export_orders_to_excel

from config import Settings

router = Router()

order_service = OrderService()
user_service = UserService()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "⚙️ *Админ-панель*\n\nВыберите действие:",
        parse_mode="Markdown",
        reply_markup=admin_main_menu_kb()
    )

@router.callback_query(F.data == "admin_panel")
async def admin_panel(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return

    await callback.answer()

    await callback.message.edit_text(
        "⚙️ *Админ-панель*\n\nВыберите действие:",
        parse_mode="Markdown",
        reply_markup=admin_main_menu_kb()
    )

@router.callback_query(F.data == "admin_orders_menu")
async def admin_orders_menu(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return await callback.answer("Нет доступа", show_alert=True)

    db = SessionLocal()
    orders = order_service.get_all_open_orders(db)

    await callback.message.edit_text(
        "Управление всеми заказами",
        parse_mode="Markdown",
        reply_markup=admin_orders_page_kb(orders, page=0)
    )

    await callback.answer()


@router.callback_query(F.data.startswith("admin_page_"))
async def admin_page(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return await callback.answer("Нет доступа", show_alert=True)

    page = int(callback.data.replace("admin_page_", ""))

    db = SessionLocal()
    open_orders = order_service.get_all_open_orders(db)
    closed_orders = order_service.get_all_closed_orders(db)

    all_orders = open_orders + closed_orders

    await callback.message.edit_reply_markup(
        reply_markup=admin_orders_page_kb(all_orders, page=page)
    )

    await callback.answer()


@router.callback_query(F.data.startswith("admin_order_"))
async def admin_show_order(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return await callback.answer("Нет доступа", show_alert=True)

    order_id = int(callback.data.replace("admin_order_", ""))
    db = SessionLocal()
    order = order_service.get_order(db, order_id)

    user = user_service.repo.get_user_by_db_id(db, order.user_id)

    text = (
        f"📝 *Заказ №{order.id}* создан {order.created_at}\n\n"
        f"*Пользователь*:\n"
        f" ├ @{user.username or 'нет'}\n"
        f" └ ID: {user.chat_id}\n\n"
        
        f"*Получатель*:\n"
        f" └ {order.full_name}\n\n"

        f"*Детали заказа*:\n"
        f" ├ Модель: {order.name}\n"
        f" ├ Количество: {order.quantity}\n"
        f" ├ Материал: {order.material}\n"
        f" ├ Цвет: {order.color}\n"
        f" └ Пожелания: {order.notes or 'нет'}\n\n"

        f"*Цена*:\n"
        f" ├ {order.price_rub} ₽ всего\n"
        f" └ {order.unit_price_rub} ₽ за 1 шт.\n\n"

        f"Статус заказа: *{Settings.human_status.get(order.status, order.status.value)}*"
    )


    try:
        await callback.message.delete()
    except:
        pass

    stl = FSInputFile(order.stl_path)

    await callback.message.answer_document(
        document=stl,
        caption=text,
        parse_mode="Markdown",
        reply_markup=admin_order_actions_kb(order_id)
    )

    await callback.answer()



@router.callback_query(F.data == "admin_back_to_orders")
async def admin_back(callback: CallbackQuery):
    db = SessionLocal()
    orders = order_service.get_all_orders(db)

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        "*Список заказов:*",
        parse_mode="Markdown",
        reply_markup=admin_orders_page_kb(orders, page=0)
    )

    await callback.answer()


@router.callback_query(F.data.startswith("admin_change_status_"))
async def admin_change_status(callback: CallbackQuery):
    order_id = int(callback.data.replace("admin_change_status_", ""))

    await callback.message.edit_caption(
        caption="Выберите новый статус:",
        reply_markup=admin_status_select_kb(order_id)
    )

    await callback.answer()


@router.callback_query(F.data.startswith("admin_set_status_"))
async def admin_set_status(callback: CallbackQuery):
    parts = callback.data.split("_")
    order_id = int(parts[3])
    new_status = parts[4]

    text = (
        f"Подтвердить изменение статуса заказа #{order_id} "
        f"на *{new_status}*?"
    )

    await callback.message.edit_caption(
        caption=text,
        parse_mode="Markdown",
        reply_markup=admin_confirm_status_kb(order_id, new_status)
    )

    await callback.answer()


@router.callback_query(F.data.startswith("admin_confirm_status_"))
async def admin_confirm_status(callback: CallbackQuery, bot: Bot):
    parts = callback.data.split("_")
    order_id = int(parts[3])
    new_status = parts[4]

    db = SessionLocal()
    order = order_service.update_order_status(db, order_id, OrderStatus(new_status))

    user = user_service.repo.get_user_by_db_id(db, order.user_id)

    try:
        await bot.send_message(
            chat_id=user.chat_id,
            text=(
                f"🔔 *Обновление статуса заказа*\n\n"
                f"Статус вашего заказа №*{order_id}* был изменён на:\n"
                f"*{Settings.human_status.get(OrderStatus(new_status), order.status.value)}*"
            ),
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Не удалось отправить уведомление пользователю: {e}")

    await callback.message.edit_caption(
        caption=f"Статус заказа #{order_id} успешно изменён на *{Settings.human_status.get(OrderStatus(new_status), order.status.value)}*",
        parse_mode="Markdown",
        reply_markup=admin_order_actions_kb(order_id)
    )

    await callback.answer("Статус обновлен")

@router.callback_query(F.data == "admin_export_excel")
async def admin_export_excel(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return await callback.answer("Нет доступа", show_alert=True)

    db = SessionLocal()
    orders = order_service.get_all_orders(db)

    filepath = "orders_export.xlsx"
    export_orders_to_excel(orders, filepath)

    await callback.message.answer_document(
        FSInputFile(filepath),
        caption="Ваш excel файл со всеми заказами."
    )

    await callback.answer()
