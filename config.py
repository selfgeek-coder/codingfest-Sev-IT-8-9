from dotenv import load_dotenv
from os import getenv

from app.enums.order_status import OrderStatus

load_dotenv()

class Settings:
    database_url = getenv("DATABASE_URL")

    token = getenv("TOKEN")

    admins = [
        int(x.strip())
        for x in getenv("ADMINS", "").split(",")
        if x.strip().isdigit()
    ]

    hour_rate = 200          # ₽ за час работы принтера
    min_price = 150          # минимальная стоимость заказа
    electricity_rub_h = 5

    materials = {
        "PLA": {
            "density": 1.24,
            "price": 1000
        },
        "ABS": {
            "density": 1.04,
            "price": 1000
        },
        "PETG": {
            "density": 1.27,
            "price": 1200
        }
    }

    human_status = {
        OrderStatus.created: "Создан",
        OrderStatus.accepted: "Принят в обработку",
        OrderStatus.processing: "В процессе",
        OrderStatus.done: "Готов к выдаче",
        OrderStatus.delivered: "Получен клиентом",
        OrderStatus.closed: "Закрыт"
    } # человеческие обозначения с OrderStatus