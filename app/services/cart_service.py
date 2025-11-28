from app.database.repositories.cart_repository import CartRepository

class CartService:
    def __init__(self):
        self.repo = CartRepository()

    def add_to_cart(self, db, **kwargs):
        return self.repo.add_item(db, **kwargs)

    def get_cart(self, db, user_id):
        return self.repo.get_user_cart(db, user_id)

    def delete_item(self, db, item_id):
        return self.repo.delete_item(db, item_id)

    def clear_cart(self, db, user_id):
        return self.repo.clear_cart(db, user_id)
