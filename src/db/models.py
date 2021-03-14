from tortoise import Model, fields


class Flat(Model):
    id = fields.IntField(pk=True)
    url = fields.TextField(null=False)
    price = fields.IntField()
    is_published = fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
