from sqlalchemy import orm, Column, Integer, String, Boolean
from enum import Enum
from app.database import Base
from data.model.relations.user_chat import user_chat


class ChatTable(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    unseen_message_count = Column(Integer, nullable=False, default=0)
    last_message_id = Column(Integer, nullable=True)

    users = orm.relationship(
        "UserTable", secondary="user_chat", backref='chats'  
    )

    messages = orm.relationship(
        "MessageTable", back_populates="chat"
    )