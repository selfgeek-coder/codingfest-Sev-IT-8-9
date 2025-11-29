import enum

class OrderStatus(enum.Enum):
    created = "created" # при создании заказа по умолчанию
    accepted = "accepted"
    processing = "processing"
    done = "done"
    delivered = "delivered" # получен клиентом
    closed = "closed"