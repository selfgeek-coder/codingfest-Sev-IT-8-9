from aiogram.fsm.state import StatesGroup, State

class OrderFSM(StatesGroup):
    upload_file = State()
    quantity = State()
    material = State()
    color = State()
    custom_color = State()
    full_name = State()
    notes = State()
    confirm = State()