from tortoise import Model, fields


class Flat(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(null=False, max_length=2048, unique=True)
    price = fields.IntField(null=False)
    is_published = fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
