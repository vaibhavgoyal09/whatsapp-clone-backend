from sqlalchemy import orm, Column, Integer, String, ForeignKey
from data.database import Base
from .relations.user_group import user_group


class GroupTable(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String, nullable=True)
    profile_image_url = Column(String, nullable=True)
    admin_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    admin = orm.relationship("UserTable", back_populates="created_groups")

    users = orm.relationship("UserTable", secondary=user_group, back_populates="groups")

    messages = orm.relationship("MessageTable", back_populates="group")
