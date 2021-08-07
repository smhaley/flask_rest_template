from marshmallow.decorators import validates
from marshmallow.exceptions import ValidationError
from app import ma
from models import Favorites


class FavoritesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Favorites
        load_instance = True
        include_fk = True

