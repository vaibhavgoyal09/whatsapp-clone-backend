from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .relations.user_chat import user_chat
from .relations.user_group import user_group


class UserTable(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    firebase_uid = Column(String)
    name = Column(String(30))
    about = Column(String)
    profile_image_url = Column(String)
    phone_number = Column(String(20))

    statuses = relationship(
        "StatusTable", back_populates="user", cascade="all, delete-orphan"
    )

    messages = relationship(
        "MessageTable", back_populates="sender"
    )

    chats = relationship(
        "ChatTable", secondary=user_chat, back_populates="users"
    )

    groups = relationship(
        "GroupTable", secondary=user_group, back_populates='users'
    )
