from enum import Enum
from data.database import Base
from sqlalchemy import Integer, Column, String, ForeignKey, Float
from datetime import datetime
from sqlalchemy.orm import relationship
from app.model.message import MessageType

class MessageTable(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False, default=MessageType.text.value)
    message = Column(String, nullable=True)
    media_url = Column(String, nullable=True)
    created_at = Column(Integer, nullable=False, default=int(datetime.timestamp(datetime.utcnow())))
    sender_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    one_to_one_chat_id = Column(Integer, ForeignKey("one_to_one_chat.id"), nullable=True)
    group_id = Column(Integer, ForeignKey("group.id"), nullable=True)

    sender = relationship("UserTable", back_populates="messages")
    one_to_one_chat = relationship("OneToOneChatTable", back_populates="messages")
    group = relationship("GroupTable", back_populates="messages")
