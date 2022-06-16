from tortoise.models import Model
from tortoise import fields


class GroupTable(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)
    description = fields.TextField(null=True)
    profile_image_url = fields.TextField(null=True)
    admin_id = fields.IntField()

    users: fields.ManyToManyRelation['data.model.user.UserTable'] = fields.ManyToManyField(
        'models.UserTable',
        related_name='groups',
        through='user_group'
    )

    class Meta:
        table="group"
