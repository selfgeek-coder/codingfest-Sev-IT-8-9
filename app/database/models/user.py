from sqlalchemy import Column, Integer, String

from ..session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))

    def __repr__(self):
        return f"<User id={self.id}, chat_id={self.chat_id}>"
