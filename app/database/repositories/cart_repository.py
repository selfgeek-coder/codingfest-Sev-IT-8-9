from sqlalchemy.orm import Session
from ..models.cart import CartItem


class CartRepository:
    def add_item(self, db: Session, **kwargs) -> CartItem:
        item = CartItem(**kwargs)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def get_user_cart(self, db: Session, user_id: int):
        return db.query(CartItem).filter(CartItem.user_id == user_id).all()

    def delete_item(self, db: Session, item_id: int):
        item = db.query(CartItem).filter(CartItem.id == item_id).first()
        if item:
            db.delete(item)
            db.commit()

    def clear_cart(self, db: Session, user_id: int):
        db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        db.commit()
