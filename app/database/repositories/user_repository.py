from sqlalchemy.orm import Session
from ..models.user import User


class UserRepository:
    def create_user(
        self,
        db: Session,
        chat_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> User:

        user = User(
            chat_id=chat_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def update_user(
        self,
        db: Session,
        user: User,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> User:

        if username is not None:
            user.username = username

        if first_name is not None:
            user.first_name = first_name

        if last_name is not None:
            user.last_name = last_name

        db.commit()
        db.refresh(user)
        
        return user

    def delete_user(self, db: Session, user: User) -> None:
        db.delete(user)
        db.commit()

    def get_user_by_id(self, db: Session, chat_id: int) -> User | None:
        return db.query(User).filter(User.chat_id == chat_id).first()
