from tortoise.models import Model
from tortoise import fields
from enum import Enum


class ChatType(Enum):
    one_to_one = 0
    group = 1


class ChatTable(Model):
    id = fields.IntField(pk=True)
    type = fields.IntField(default=ChatType.one_to_one.value)
    is_pinned = fields.BooleanField(default=False)
    unseen_message_count = fields.IntField(default=0)
    last_message_id = fields.IntField(null=True)
    group_id = fields.IntField(null=True)

    user = fields.ForeignKeyField(
        'models.UserTable',
        related_name = "chats"
    )

    messages: fields.ReverseRelation['data.model.message']

    class Meta:
        table = "chat"