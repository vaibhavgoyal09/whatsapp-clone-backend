from sqlalchemy import orm, Column, Integer, String, Boolean
from enum import Enum
from app.database import Base
from data.model.relations.user_chat import user_chat


class ChatType(Enum):
    one_to_one = 0
    group = 1


class ChatTable(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False, default=ChatType.one_to_one.value)
    unseen_message_count = Column(Integer, nullable=False, default=0)
    last_message_id = Column(Integer, nullable=True)
    group_id = Column(Integer, nullable=True)

    users = orm.relationship(
        "UserTable", secondary="user_chat", backref='chats'  
    )

    messages = orm.relationship(
        "MessageTable", back_populates="chat"
    )