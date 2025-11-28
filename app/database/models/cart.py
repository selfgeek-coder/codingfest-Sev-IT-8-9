from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from ..session import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")

    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    material = Column(String(50), nullable=False)
    color = Column(String(100), nullable=False)
    full_name = Column(String(255), nullable=False)
    notes = Column(String(500))
    stl_path = Column(String(500), nullable=False)

    price_rub = Column(Float, nullable=False)
    unit_price_rub = Column(Float, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Europe/Moscow"))
    )

    def __repr__(self):
        return f"<CartItem {self.id} user={self.user_id}>"
