from dotenv import load_dotenv
from os import getenv

from app.enums.order_status import OrderStatus

load_dotenv()

class Settings:
    database_url = getenv("DATABASE_URL")
    token = getenv("TOKEN")

    densities = {
        "PLA": 1.24,
        "ABS": 1.04,
        "PETG": 1.27
    }

    prices = {
        "PLA": 1000,
        "ABS": 1000,
        "PETG": 1200
    }

    human_status = {
        OrderStatus.created: "🆕 Создан",
        OrderStatus.processing: "В процессе разработки...",
        OrderStatus.done: "✅ Завершен и готов к выдаче"
    } # человеческие обозначения с OrderStatus