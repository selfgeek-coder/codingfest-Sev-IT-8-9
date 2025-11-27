from sqlalchemy.orm import Session

from app.enums.order_status import OrderStatus
from app.database.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self):
        self.repo = OrderRepository()

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
            ):
        """
        создает заказ
        """

        return self.repo.create_order(
            db=db,
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


    def get_order(self, db: Session, order_id: int):
        """
        получить заказ по ID
        """

        return self.repo.get_order_by_id(db, order_id)

    def delete_order(self, db: Session, order_id: int) -> bool:
        """
        удаляет заказ по его ID
        """

        order = self.repo.get_order_by_id(db, order_id)
        if not order:
            return False

        self.repo.delete_order(db, order)
        return True

    def get_user_orders(self, db: Session, user_id: int):
        """
        получить все заказы пользователя по его user_id
        """

        return self.repo.get_orders_by_user(db, user_id)
    

    def update_order_status(self, db: Session, order_id: int, new_status: OrderStatus):
        """
        меняет статус заказа
        """

        order = self.repo.get_order_by_id(db, order_id)
        if not order:
            return None  

        return self.repo.update_order_status(db, order, new_status)

    def get_all_orders(self, db: Session):
        return self.repo.get_all_orders(db)

    def get_all_open_orders(self, db: Session):
        return self.repo.get_all_open_orders(db)

    def get_all_closed_orders(self, db: Session):
        return self.repo.get_all_closed_orders(db)
