from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models.orders import Order


class OrderRepository:
    def create_order(
                self,
                db: Session,
                user_id: int,
                quantity: int,
                material: str,
                color: str,
                full_name: str,
                notes: str,
                stl_path: str,
                price_rub: float,
                unit_price_rub: float
            ) -> Order:

        order = Order(
            user_id=user_id,
            quantity=quantity,
            material=material,
            color=color,
            full_name=full_name,
            notes=notes,
            stl_path=stl_path,
            price_rub=price_rub,
            unit_price_rub=unit_price_rub
        )

        db.add(order)
        db.commit()
        db.refresh(order)
        return order


    def get_order_by_id(self, db: Session, order_id: int) -> Order | None:
        return db.query(Order).filter(Order.id == order_id).first()

    def delete_order(self, db: Session, order: Order) -> None:
        db.delete(order)
        db.commit()

    def get_orders_by_user(self, db: Session, user_id: int) -> list[Order]:
        return db.query(Order).filter(Order.user_id == user_id).all()
