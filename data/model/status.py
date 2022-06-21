from data.database import Base
from sqlalchemy import Integer, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import datetime


class StatusType(Enum):
    image = 0
    video = 1


class StatusTable(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    type = Column(Integer, default=StatusType.image.value, nullable=False)
    media_url = Column(String, nullable=False)
    created_at = Column(DateTime, default= datetime.utcnow, nullable=False) 
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("UserTable", back_populates="statuses")