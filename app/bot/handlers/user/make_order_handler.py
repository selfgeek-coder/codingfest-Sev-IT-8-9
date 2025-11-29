import os
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.utils import gen_random_name, validate_fullname
from app.services.calc_service import CalcService
from app.database.session import SessionLocal
from app.services.user_service import UserService
from app.services.cart_service import CartService
from ...bot_utils import send_clean_message
from ...states.order_fsm import OrderFSM

from app.bot.keyboards.user.make_order_kb import (
    cancel_kb,
    material_kb,
    color_kb,
    skip_kb,
    confirm_kb
)

from app.bot.keyboards.user.cart_kb import cart_menu_kb


router = Router()

user_service = UserService()
cart_service = CartService()


# начало оформления: запрашивваем файл модели
@router.callback_query(F.data == "make_order")
async def start_order(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await send_clean_message(
        callback,
        bot,
        state,
        "Отправьте .stl файл вашей модели.",
        reply_markup=cancel_kb()
    )

    await state.set_state(OrderFSM.upload_file)

    await callback.answer()


# загружаем файл модели и получаем количество моделей
@router.message(OrderFSM.upload_file, F.document)
async def get_stl(message: Message, state: FSMContext, bot: Bot):
    if not message.document.file_name.lower().endswith(".stl"):
        return await send_clean_message(
            message,
            bot,
            state,
            "Отправьте файл формата .stl"
        )

    os.makedirs("files", exist_ok=True)
    file = await bot.get_file(message.document.file_id)

    name = os.path.splitext(message.document.file_name)[0]
    path = f"files/{gen_random_name(name)}.stl"

    await bot.download(file, destination=path)

    await state.update_data(stl_path=path, file_name=name)
    await state.set_state(OrderFSM.quantity)

    await send_clean_message(
        message,
        bot,
        state,
        "Введите количество моделей:",
        reply_markup=cancel_kb()
    )


# получили количество, получаем тип пластика (из конфигурации)
@router.message(OrderFSM.quantity)
async def get_quantity(message: Message, state: FSMContext, bot: Bot):
    if not message.text.isdigit():
        return await send_clean_message(
            message,
            bot,
            state,
            "Введите число.",
            reply_markup=cancel_kb()
        )

    await state.update_data(quantity=int(message.text))
    await state.set_state(OrderFSM.material)

    await send_clean_message(
        message,
        bot,
        state,
        "Выберите тип пластика:",
        reply_markup=material_kb()
    )


# получили тип пластика, получаем цвет модели
@router.callback_query(F.data.startswith("mat_"), OrderFSM.material)
async def get_material(callback: CallbackQuery, state: FSMContext, bot: Bot):
    material = callback.data.replace("mat_", "")
    await state.update_data(material=material)

    await state.set_state(OrderFSM.color)

    await send_clean_message(
        callback,
        bot,
        state,
        "Выберите цвет модели:",
        reply_markup=color_kb()
    )
    await callback.answer()


@router.callback_query(F.data == "color_custom", OrderFSM.color)
async def custom_color(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await send_clean_message(
        callback,
        bot,
        state,
        "Введите свой цвет модели:",
        reply_markup=cancel_kb()
    )
    await state.set_state(OrderFSM.custom_color)
    await callback.answer()


@router.message(OrderFSM.custom_color)
async def get_custom_color(message: Message, state: FSMContext, bot: Bot):

    await state.update_data(color=message.text)

    await send_clean_message(
        message,
        bot,
        state,
        "Введите ваше имя и фамилию в формате:\n*Иван Иванов*",
        parse_mode="Markdown",
        reply_markup=cancel_kb()
    )
    
    await state.set_state(OrderFSM.full_name)


@router.callback_query(F.data.startswith("color_"), OrderFSM.color)
async def get_color(callback: CallbackQuery, state: FSMContext, bot: Bot):
    color = callback.data.replace("color_", "")
    await state.update_data(color=color)

    await send_clean_message(
        callback,
        bot,
        state,
        "Введите ваше имя и фамилию в формате:\n*Иван Иванов*",
        parse_mode="Markdown",
        reply_markup=cancel_kb()
    )
    await state.set_state(OrderFSM.full_name)
    await callback.answer()


# получаем дополнительные пожелания (опционально)
@router.message(OrderFSM.full_name)
async def get_fullname(message: Message, state: FSMContext, bot: Bot):
    if not validate_fullname(message.text):
        return await send_clean_message(
            message,
            bot,
            state,
            "Введите корректное ФИ:\n*Иван Иванов*",
            parse_mode="Markdown",
            reply_markup=cancel_kb()
        )

    await state.update_data(full_name=message.text)

    await send_clean_message(
        message,
        bot,
        state,
        "Добавьте пожелания или нажмите *Пропустить*",
        parse_mode="Markdown",
        reply_markup=skip_kb()
    )
    await state.set_state(OrderFSM.notes)


@router.callback_query(F.data == "skip_notes", OrderFSM.notes)
async def skip_notes(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(notes="-")

    data = await state.get_data()
    await preview_order(callback, data, bot, state)

    await state.set_state(OrderFSM.confirm)
    await callback.answer()


@router.message(OrderFSM.notes)
async def get_notes(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(notes=message.text)

    data = await state.get_data()

    await preview_order(message, data, bot, state)

    await state.set_state(OrderFSM.confirm)


async def preview_order(message_or_callback, data, bot: Bot, state: FSMContext):
    calc = CalcService.calc_price(
        file_path=data["stl_path"],
        material=data["material"],
        speed=60
    )

    data["price_one"] = calc["price_rub"]
    data["total_price"] = calc["price_rub"] * data["quantity"]

    summary = (
        "Ваш заказ:\n\n"
        f"├ Количество: {data['quantity']}\n"
        f"├ Пластик: {data['material']}\n"
        f"├ Цвет: {data['color']}\n"
        f"├ ФИ: {data['full_name']}\n"
        f"└ Пожелания: {data.get('notes', '-')}\n\n"
        "Стоимость:\n"
        f"├ За 1 шт: ~{round(data['price_one'])} ₽\n"
        f"└ За всё: ~{round(data['total_price'])} ₽\n\n"
        "*Добавить в корзину?*"
    )

    await send_clean_message(
        message_or_callback,
        bot,
        state,
        summary,
        reply_markup=confirm_kb(),
        parse_mode="Markdown"
    )


# предосмотр товара, подтверждение и добавление в корзину
@router.callback_query(F.data == "confirm_yes", OrderFSM.confirm)
async def confirm_order(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
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

    calc = CalcService.calc_price(
        file_path=data["stl_path"],
        material=data["material"],
        speed=60
    )

    data["price_one"] = calc["price_rub"]
    data["total_price"] = calc["price_rub"] * data["quantity"]

    cart_service.add_to_cart(
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

    await send_clean_message(
        callback,
        bot,
        state,
        "Товар успешно добавлен в вашу корзину.\n\nМожете оформить заказ или добавить еще один заказ в корзину.",
        reply_markup=cart_menu_kb()
    )

    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "confirm_no", OrderFSM.confirm)
async def confirm_no(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()

    await send_clean_message(
        callback,
        bot,
        state,
        "Хорошо. Отправьте новый STL файл:",
        reply_markup=cancel_kb()
    )

    await state.set_state(OrderFSM.upload_file)
    await callback.answer()


@router.callback_query(F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer("Заказ отменен")
    try:
        await callback.message.delete()
    except:
        pass
        