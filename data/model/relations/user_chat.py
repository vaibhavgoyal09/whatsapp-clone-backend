from sqlalchemy import Table, Column, ForeignKey
from app.database import Base


user_chat = Table(
    "user_chat",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("chat_id", ForeignKey("chat.id"), primary_key=True)
)