from enum import Enum
from app.database import Base
from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship


class MessageType(Enum):
    text = 0
    audio = 1
    video = 2
    gif = 3


class MessageTable(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False, default=MessageType.text.value)
    message = Column(String, nullable=True)
    media_url = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    sender_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    chat_id = Column(Integer, ForeignKey("chat.id"), nullable=False)

    sender = relationship("UserTable", back_populates="messages")
    chat = relationship("ChatTable", back_populates="messages")