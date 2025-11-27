from sqlalchemy.orm import Session
from sqlalchemy import select

from app.enums.order_status import OrderStatus
from ..models.orders import Order


class OrderRepository:
    def create_order(
                self,
                db: Session,
                user_id: int,
                name: str,
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
            name=name,
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

    def update_order_status(self, db: Session, order: Order, new_status: OrderStatus) -> Order:
        order.status = new_status
        db.commit()
        db.refresh(order)
        return order
    
    def get_all_open_orders(self, db: Session) -> list[Order]:
        return (
            db.query(Order)
            .filter(Order.status != OrderStatus.closed)
            .order_by(Order.id.desc())
            .all()
        )


    def get_all_closed_orders(self, db: Session) -> list[Order]:
        return (
            db.query(Order)
            .filter(Order.status == OrderStatus.closed)
            .order_by(Order.id.desc())
            .all()
        )

    def get_all_orders(self, db: Session) -> list[Order]:
        return (
            db.query(Order)
            .order_by(Order.id.desc())
            .all()
        )