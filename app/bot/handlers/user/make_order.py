from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

import os
import logging

from app.bot.keyboards.user.make_order_menu import (
    cancel_kb,
    material_kb,
    color_kb,
    skip_kb,
    confirm_kb,
    my_orders_kb
)

from app.services.calc_service import CalcService
from app.database.session import SessionLocal
from app.services.user_service import UserService
from app.services.order_service import OrderService
from app.utils import gen_random_name, validate_fullname
from ...states.order_fsm import OrderFSM
from config import Settings

router = Router()

user_service = UserService()
order_service = OrderService()

# запрос .stl файла
@router.callback_query(F.data == "make_order")
async def start_order(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Отправьте STL файл вашей модели.",
        reply_markup=cancel_kb()
    )
    await state.set_state(OrderFSM.upload_file)
    await callback.answer()

# сохранение .stl файла и получение количества моделей
@router.message(OrderFSM.upload_file, F.document)
async def get_stl(message: Message, state: FSMContext, bot: Bot):
    if not message.document.file_name.lower().endswith(".stl"):
        return await message.answer("Пожалуйста, отправьте файл формата .stl")

    processing_msg = await message.answer("⌛")

    os.makedirs("files", exist_ok=True)
    file = await bot.get_file(message.document.file_id)

    # имя файла без .stl
    original_name = os.path.splitext(message.document.file_name)[0]

    # генерируем уникальный путь для сохранения
    path = f"files/{gen_random_name(original_name)}.stl"

    await bot.download(file, destination=path)

    await state.update_data(stl_path=path, file_name=original_name)

    await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)

    await message.answer(
        "✅ Файл получен. Теперь введите количество моделей:",
        reply_markup=cancel_kb()
    )
    await state.set_state(OrderFSM.quantity)



# получили количество, получаем вид пластика
@router.message(OrderFSM.quantity)
async def get_quantity(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Введите число.", reply_markup=cancel_kb())

    await state.update_data(quantity=int(message.text))

    await message.answer("Выберите пластик:", reply_markup=material_kb())

    await state.set_state(OrderFSM.material)


# получили пластик, получаем цвет
@router.callback_query(F.data.startswith("mat_"), OrderFSM.material)
async def get_material(callback: CallbackQuery, state: FSMContext):
    material = callback.data.replace("mat_", "")
    await state.update_data(material=material)

    await callback.message.edit_text(
        "Выберите цвет модели:",
        reply_markup=color_kb()
    )

    await state.set_state(OrderFSM.color)

    await callback.answer()

# получение кастомного цвета
@router.callback_query(F.data == "color_custom", OrderFSM.color)
async def choose_custom_color(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Введите свой цвет модели текстом (например, 'розовый'):",
        reply_markup=cancel_kb()
    )

    await state.set_state(OrderFSM.custom_color)

    await callback.answer()

# получили кастом цвет пластика, получаем ФИ
@router.message(OrderFSM.custom_color)
async def get_custom_color(message: Message, state: FSMContext):
    await state.update_data(color=message.text)

    await message.answer(
        "Введите ваше имя и фамилию:",
        reply_markup=cancel_kb()
    )
    await state.set_state(OrderFSM.full_name)

# получили цвет пластика, получаем ФИ
@router.callback_query(F.data.startswith("color_"), OrderFSM.color)
async def get_color(callback: CallbackQuery, state: FSMContext):
    color = callback.data.replace("color_", "")
    await state.update_data(color=color)

    await callback.message.edit_text(
        "Введите ваше имя и фамилию:",
        reply_markup=cancel_kb()
    )
    await state.set_state(OrderFSM.full_name)
    await callback.answer()


# получаем дополнительные пожелания
@router.message(OrderFSM.full_name)
async def get_fullname(message: Message, state: FSMContext):
    if not validate_fullname(message.text):
        return await message.answer(
            "Пожалуйста, введите корректные имя и фамилию.\n"
            "Пример: *Иван Петров*",
            parse_mode="Markdown",
            reply_markup=cancel_kb()
        )

    await state.update_data(full_name=message.text)

    await message.answer(
        "Добавьте дополнительные пожелания или нажмите 'Пропустить':",
        reply_markup=skip_kb()
    )
    await state.set_state(OrderFSM.notes)


@router.callback_query(F.data == "skip_notes", OrderFSM.notes)
async def skip_notes(callback: CallbackQuery, state: FSMContext):
    await state.update_data(notes="-")

    data = await state.get_data()
    await preview_order(callback.message, data)

    await state.set_state(OrderFSM.confirm)
    await callback.answer()


@router.message(OrderFSM.notes)
async def get_notes(message: Message, state: FSMContext):
    await state.update_data(notes=message.text)

    data = await state.get_data()
    await preview_order(message, data)

    await state.set_state(OrderFSM.confirm)


async def preview_order(sender, data):
    calc = CalcService.calc_price(
        file_path=data["stl_path"],
        material=data["material"],
        speed=60
    )

    data["price_one"] = calc["price_rub"]
    data["total_price"] = calc["price_rub"] * data["quantity"]

    summary = (
        f"Ваш заказ:\n\n"
        f"*Количество моделей*: {data['quantity']}\n"
        f"*Пластик*: {data['material']}\n"
        f"*Цвет модели*: {data['color']}\n"
        f"*Ваше ФИ*: {data['full_name']}\n"
        f"*Доп. пожелания*: {data.get('notes', '-')}\n\n"
        f"*Примерный расчет стоимости заказа*:\n"
        f"*Объём*: {calc['volume_cm3']} см³\n"
        f"*Вес*: {calc['weight_g']} г\n"
        f"*Цена за 1 шт*: ~{data['price_one']} ₽\n"
        f"*Цена за {data['quantity']} шт*: ~{data['total_price']} ₽\n\n"
        f"*Все верно?*"
    )

    await sender.answer(summary, parse_mode="Markdown", reply_markup=confirm_kb())


# если пользователь подтвердил
@router.callback_query(F.data == "confirm_yes", OrderFSM.confirm)
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    processing_msg = await callback.message.answer("⌛")

    data = await state.get_data()

    calc = CalcService.calc_price(
        file_path=data["stl_path"],
        material=data["material"],
        speed=60
    )

    data["price_one"] = calc["price_rub"]
    data["total_price"] = calc["price_rub"] * data["quantity"]

    db = SessionLocal()


    user = user_service.repo.get_user_by_chat_id(db, callback.from_user.id)

    if not user:
        user = user_service.create_user(
            db=db,
            chat_id=callback.from_user.id,
            username=callback.from_user.username,
            first_name=callback.from_user.first_name,
            last_name=callback.from_user.last_name
        )

    order = order_service.create_order(
        db=db,
        user_id=user.id,
        name=data["file_name"],
        quantity=data["quantity"],
        material=data["material"],
        color=data["color"],
        full_name=data["full_name"],
        notes=data.get("notes", "-"),
        stl_path=data["stl_path"],
        price_rub=data["total_price"],
        unit_price_rub=data["price_one"]
    )

    try:
        # отправляем сообщение администратор(ам)
        text = (
            f"Поступил *Новый заказ* #{order.id} от @{callback.from_user.username or 'без username'} (ID {callback.from_user.id})\n\n"
            f"*Название*: {data["file_name"]}\n\n"
            f"*Количество моделей*: {data['quantity']}\n\n"
            f"*Пластик*: {data['material']}\n"
            f"*Цвет*: {data['color']}\n\n"
            f"*Сумма заказа*: {data['total_price']} ₽\n\n"
            f"*Подробнее можно посмотреть в админ-панели (/admin)*"
        )

        for admin in Settings.admins:
            await callback.bot.send_message(
                chat_id=admin,
                text=text,
                parse_mode="Markdown"
            )

            stl_file = FSInputFile(data["stl_path"])

            try:
                await callback.bot.send_document(
                    chat_id=admin,
                    document=stl_file,
                    caption=f"*STL файл* для заказа #{order.id}",
                    parse_mode="Markdown"
                )
                
            except Exception as e:
                logging.error(f"Ошибка при отправки .stl файла администратору: {e}")


    except Exception as e:
        logging.error("Ошибка отправки уведомления админу:", e)

    await processing_msg.delete()

    await callback.message.edit_text(
        f"Ваш заказ *№{order.id}* успешно сохранен!\n\n"
        f"Отслеживать статус заказа вы можете в разделе 'Мои заказы'.",
        parse_mode="Markdown",
        reply_markup=my_orders_kb()
    )
    
    await state.clear()
    await callback.answer()

# если пользователь не подтвердил
@router.callback_query(F.data == "confirm_no", OrderFSM.confirm)
async def confirm_no(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.edit_text(
        "Хорошо, начнем заново.\nОтправьте STL файл вашей модели:",
        reply_markup=cancel_kb()
    )

    await state.set_state(OrderFSM.upload_file)
    await callback.answer()

# хендлер кнопки 'Отмена'
@router.callback_query(F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    
    await callback.answer("Заказ отменен", show_alert=False)

    try:
        await callback.message.delete()

    except:
        pass