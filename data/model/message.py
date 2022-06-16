from tortoise.models import Model
from tortoise import fields
from enum import Enum


class MessageType(Enum):
    text = 0
    audio = 1
    video = 2
    gif = 3


class MessageTable(Model):
    id = fields.IntField(pk=True)
    type = fields.IntField(default=MessageType.text.value)
    message = fields.TextField(null=True)
    media_url = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    sender = fields.ForeignKeyField(
        'models.UserTable',
        related_name='messages'
    )

    chat = fields.ForeignKeyField(
        'models.ChatTable',
        related_name='messages'
    )

    class Meta:
        table = 'message'