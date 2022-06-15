from tortoise.models import Model
from tortoise import fields


class UserTable(Model):
    id = fields.IntField(pk=True)
    firebase_uid = fields.TextField()
    name = fields.CharField(max_length=40)
    about = fields.TextField()
    profile_image_url = fields.TextField()
    phone_number = fields.CharField(max_length=20)

    class Meta:
        table = "user"