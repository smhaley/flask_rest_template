from marshmallow.decorators import validates
from marshmallow.exceptions import ValidationError
from app import ma
from models import Location


class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True

    @validates('lat')
    def validate_lat(self, lat):
        if lat > 90 or lat < -90:
            raise ValidationError('The latitude is outside of range.')

    @validates('lon')
    def validate_lon(self, lon):
        if lon > 180 or lon < -180:
            raise ValidationError('The longitude is outside of range.')
