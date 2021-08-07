from flask import make_response, abort
from models import Favorites
from .favorites_schema import FavoritesSchema
from app import db
from marshmallow.exceptions import ValidationError
from utils.utils import get_lim_offset


def read_all(user_id, **kwargs):
    """
    This function responds to a request for /api/favorites/user/{user_id}
    with the complete lists of a given users favorites
    :param user_id:  user_id of the user
    :return:        json list of list of all a users favorites
    """
    limit, offset = get_lim_offset(kwargs)

    favorites = Favorites.query.filter(
        Favorites.user_id == user_id).order_by(Favorites.id).limit(limit).offset(offset).all()
    favorites_schema = FavoritesSchema(many=True)
    data = favorites_schema.dump(favorites)
    return data


def delete(user_id, loc_id):
    """
    This function responds to a DELETE request for /api/favorites/user/{user_id}
    deleting a users favorite given a location id from the favorites structure
    :param loc_id:   location id of specific location
    :param user_id:  user_id of the user
    :return:            200 on successful delete, 404 if not found
    """

    favorite = (
        Favorites.query.filter(Favorites.user_id == user_id,
                               Favorites.loc_id == loc_id).one_or_none()
    )

    if favorite is not None:
        db.session.delete(favorite)
        db.session.commit()
        return make_response(
            f"successfully deleted location id {loc_id} from user id {user_id} favorites", 200
        )
    else:
        abort(
            404, "{id} not found"
        )


def create(user_id, body):
    """
    This function responds to a POSTr equest for /api/favorites/user/{user_id}
    creating a new favorite in the favorites structure
    based on the passed in favorite data
    :param user_id:  user_id of the user
    :param body:    body to create in favorite structure
    :return:        201 on success, 406 on user exists
    """

    existing_favorite = (
        Favorites.query.filter(Favorites.user_id == user_id,
                               Favorites.loc_id == body.get('loc_id')).one_or_none()
    )

    if existing_favorite is None:

        try:
            schema = FavoritesSchema()
            body['user_id'] = user_id

            new_favorite = schema.load(body, session=db.session)

            db.session.add(new_favorite)
            db.session.commit()

            data = schema.dump(new_favorite)

            return data, 201

        except ValidationError as e:
            abort(400, str(e))

    else:
        abort(406, 'location already exists')
