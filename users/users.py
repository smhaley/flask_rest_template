from flask import make_response, abort
from models import Users
from .users_schema import UsersSchema
from app import db
from marshmallow.exceptions import ValidationError
from utils.utils import get_lim_offset


def read_all(**kwargs):
    """
    This function responds to a request for /api/users
    with the complete lists of users
    :return:        json list of list of users
    """
    if 'limit' in kwargs and 'offset' in kwargs:
        offset = int(kwargs['offset'])
        if kwargs['limit'] > 100 or kwargs['limit'] < 0:
            limit = 100
        else:
            limit = int(kwargs['limit'])
    else:
        limit = None
        offset = None
    
    limit, offset = get_lim_offset(kwargs)

    users = Users.query.order_by(Users.id).limit(limit).offset(offset).all()
    users_schema = UsersSchema(many=True)
    data = users_schema.dump(users)
    return data


def read_one(id):
    """
    This function responds to a PUT equest for /api/users/{id} 
    with one matching user from users
    :param id           Id of user to find
    :return:            user matching id
    """
    user = (
        Users.query.filter(Users.id == id).one_or_none()
    )
    if user is not None:
        users_schema = UsersSchema()

        data = users_schema.dump(user)
        return data
    else:
        abort(
            404, f"{id} not found"
        )


def update(id, body):
    """
    This function responds to a PUT equest for /api/users/{id} 
    updating an existing users email and/or name in the users structure
    :param user_id:   Id of the user to update in the users structure
    :param body:      user info to update
    :return:          updated user structure
    """

    update_user = (
        Users.query.filter(Users.id == id).one_or_none()
    )

    if update_user is not None:

        email_check = Users.query.filter(
            Users.id != id, Users.email == body['email']).one_or_none()

        if email_check:
            abort(
                404, f"{body['email']} taken by another user"
            )

        try:
            users_schema = UsersSchema()

            update = users_schema.load(body, session=db.session)
            update.id = update_user.id

            db.session.merge(update)
            db.session.commit()

            return body, 201

        except ValidationError as e:

            abort(400, str(e))

    else:
        abort(
            404, f"{id} not found"
        )


def delete(id):
    """
    This function responds to a DELETE request for /api/users/{id} 
    deleting a user from the users structure
    :param user_id:     Id of the user to delete
    :return:            200 on successful delete, 404 if not found
    """

    user = (
        Users.query.filter(Users.id == id).one_or_none()
    )

    if user is not None:
        db.session.delete(user)
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
    This function responds to a POST request for /api/users/{id} 
    creating a new user in the users structure
    :param body:   user to create in users structure
    :return:       201 on success, 406 on user exists
    """

    existing_user = (
        Users.query.filter(Users.email == body.get('email')).one_or_none()
    )
    if existing_user is None:

        try:
            schema = UsersSchema()

            new_user = schema.load(body, session=db.session)
            db.session.add(new_user)
            db.session.commit()

            data = schema.dump(new_user)

            return data, 201
        except ValidationError as e:

            abort(400, str(e))

    else:
        abort(406, 'User already exists')
