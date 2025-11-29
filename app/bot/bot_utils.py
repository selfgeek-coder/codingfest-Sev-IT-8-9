from aiogram import F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

async def send_clean_message(message_or_callback, bot: Bot, state: FSMContext, text: str,
                             reply_markup=None, parse_mode=None):
    data = await state.get_data()

    chat_id = (message_or_callback.message.chat.id
               if isinstance(message_or_callback, CallbackQuery)
               else message_or_callback.chat.id)

    # удалить прошлое сообщение бота
    last_msg = data.get("last_bot_msg")
    if last_msg:
        try:
            await bot.delete_message(chat_id, last_msg)
        except:
            pass

    # отправить новое
    sent = await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )

    await state.update_data(last_bot_msg=sent.message_id)
    return sent