from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship

from ..session import Base
from ...enums.order_status import OrderStatus


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")

    quantity = Column(Integer, nullable=False)
    material = Column(String(50), nullable=False)
    color = Column(String(100), nullable=False)
    full_name = Column(String(255), nullable=False)
    notes = Column(String(500))
    stl_path = Column(String(500), nullable=False)

    price_rub = Column(Float, nullable=False)   # общая цена
    unit_price_rub = Column(Float, nullable=False)  # цена за 1 штуку

    status = Column(
        Enum(OrderStatus, name="order_status_enum"),
        nullable=False,
        default=OrderStatus.created
    )

    def __repr__(self):
        return f"<Order id={self.id} user_id={self.user_id}>"

