from marshmallow.decorators import validates
from marshmallow.exceptions import ValidationError
from app import ma
from models import Reviews


class ReviewsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reviews
        load_instance = True
        include_fk = True
    
    @validates('review')
    def validate_lat(self, review):
        if review > 5 or review < 0:
            raise ValidationError('The review is outside of range.')


    