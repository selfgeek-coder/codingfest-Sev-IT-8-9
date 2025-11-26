from sqlalchemy.orm import Session
from app.database.repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def create_user(
        self,
        db: Session,
        chat_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ):
        """
        добавляет пользователя в базу, обновляет если данные сменились, если данные не поменялись - возвращает
        """

        user = self.repo.get_user_by_id(db, chat_id)

        if user:
            new_data = {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            }

            need_update = any(
                getattr(user, field) != value
                for field, value in new_data.items()
                if value is not None
            )

            if not need_update:
                return user

            return self.repo.update_user(db, user, **new_data)

        return self.repo.create_user(
            db,
            chat_id=chat_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

    def delete_user(
            self,    
            db: Session,
            chat_id: int
        ) -> bool:
        """
        удаляет пользователя с бд по chat_id
        """

        user = self.repo.get_user_by_id(db, chat_id)
        
        if not user:
            return False

        self.repo.delete_user(db, user)
        return True
