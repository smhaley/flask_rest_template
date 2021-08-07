from flask import make_response, abort
from models import Location
from .location_schema import LocationSchema
from app import db
from marshmallow.exceptions import ValidationError
from utils.utils import loc_by_bbox, get_lim_offset


def read_all(**kwargs):
    """
    This function responds to a request for /api/location
    with the complete lists of lcoations
    :return:        json list of list of locations
    """

    limit, offset = get_lim_offset(kwargs)

    if 'ne' in kwargs and 'sw' in kwargs:
        locations = loc_by_bbox(kwargs['sw'], kwargs['ne'], limit, offset)

    elif ('sw' in kwargs and not 'ne' in kwargs) or ('ne' in kwargs and not 'sw' in kwargs):
        abort(404, 'For bbox, both ne and sw params are required')
    else:
        locations = Location.query.order_by(
            Location.id).limit(limit).offset(offset).all()
    locaiton_schema = LocationSchema(many=True)
    data = locaiton_schema.dump(locations)

    return data


def read_one(id):
    """
    This function responds to a request for /api/location/{location_id}
    with one matching user from location
    :param location_id:   Id of location to find
    :return:            location matching id
    """
    location = (
        Location.query.filter(Location.id == id).one_or_none()
    )
    if location is not None:
        location_schema = LocationSchema()

        data = location_schema.dump(location)
        return data
    else:
        abort(
            404, f"{id} not found"
        )


def update(id, body):
    """
    This function responds to a PUT request for /api/location/{location_id} 
    updating an existing location name in the location structure
    :param location_id:   Id of the location to update in the location structure
    :param body:          put body containing new name
    :return:              updated location structure
    """

    update_location = (
        Location.query.filter(Location.id == id).one_or_none()
    )

    if update_location is not None:
        body['lat'] = update_location.lat
        body['lon'] = update_location.lon

        location_schema = LocationSchema()

        update = location_schema.load(body, session=db.session)
        update.id = update_location.id

        db.session.merge(update)
        db.session.commit()

        return body, 200
    else:
        abort(
            404, f"{id} not found"
        )


def delete(id):
    """
    This function responds to a DELETE request to  /api/location/{location_id}
    deleting a location from the location structure
    :param location_id:   Id of the location to delete
    :return:            200 on successful delete, 404 if not found
    """
    location = (
        Location.query.filter(Location.id == id).one_or_none()
    )

    if location is not None:
        db.session.delete(location)
        db.session.commit()
        return make_response(
            f"successfully deleted {id}", 200
        )
    else:
        abort(
            404, "{id} not found"
        )


def create(body):
    """
    This function responds to a POST request for /api/location 
    creating a new location in the location structure
    based on the passed in location data
    :param body:    body to create in location structure
    :return:        201 on success, 406 on user exists
    """

    body['lat'] = round(body['lat'], 5)
    body['lon'] = round(body['lon'], 5)

    existing_location = (
        Location.query.filter(Location.lat == body.get(
            'lat'), Location.lon == body.get('lon')).one_or_none()
    )

    if existing_location is None:

        try:
            schema = LocationSchema()

            new_location = schema.load(body, session=db.session)
            db.session.add(new_location)
            db.session.commit()

            data = schema.dump(new_location)

            return data, 201
        except ValidationError as e:

            abort(400, str(e))

    else:
        abort(406, 'location already exists')
