from tortoise.models import Model
from tortoise import fields


class UserTable(Model):
    id = fields.IntField(pk=True)
    firebase_uid = fields.TextField()
    name = fields.CharField(max_length=40)
    about = fields.TextField(null=True)
    profile_image_url = fields.TextField(null=True)
    phone_number = fields.CharField(max_length=20)

    chats: fields.ReverseRelation['data.model.ChatTable']
    statuses: fields.ReverseRelation['data.model.status.StatusTable']
    groups: fields.ManyToManyRelation['data.model.group.GroupTable']

    class Meta:
        table = "user"