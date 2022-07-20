from sqlalchemy import orm, Column, Integer, String, Boolean, ForeignKey
from enum import Enum
from data.database import Base


class OneToOneChatTable(Base):
    __tablename__ = "one_to_one_chat"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    remote_user_id = Column(Integer, nullable=False)
    last_message_id = Column(Integer, nullable=True, default=None)

    user = orm.relationship(
        "UserTable", back_populates='one_to_one_chats'
    )

    messages = orm.relationship(
        "MessageTable", back_populates="one_to_one_chat"
    )
