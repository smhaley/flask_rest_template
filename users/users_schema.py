from app import ma
from marshmallow import fields
from models import Users


class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True

    email = fields.Email()
