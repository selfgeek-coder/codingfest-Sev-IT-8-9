import enum

class OrderStatus(enum.Enum):
    created = "created" # при создании заказа по умолчанию
    processing = "processing"
    done = "done"
    closed = "closed"