from tortoise.models import Model
from tortoise import fields
from data.model.user import UserTable
from enum import Enum


class StatusType(Enum):
    image = 0
    video = 1


class StatusTable(Model):
    id = fields.IntField(pk=True)
    type = fields.IntField(default=StatusType.image.value)
    media_url = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True) 
    
    user: fields.ForeignKeyRelation[user] = fields.ForeignKeyRelation(
        "models.UserTable",
        related_name="statuses"
    ) 

    class Meta:
        table="status"