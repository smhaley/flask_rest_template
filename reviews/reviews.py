from abc import get_cache_token
from .reviews_schema import ReviewsSchema
from flask import make_response, abort
from models import Reviews
from app import db
from marshmallow.exceptions import ValidationError
from utils.utils import loc_by_bbox, get_lim_offset


def read_all(**kwargs):
    """
    This function responds to a request for /api/reviews
    returning the complete lists of reviews based on query parameters
    Query params are required
    :params:
        BBox using sw and ne inputing a string tuple '(lat, long)'
        user_id
        loc_id
    :return:   json list of list of reviews reflecting query
    """

    limit, offset = get_lim_offset(kwargs)

    if 'ne' in kwargs and 'sw' in kwargs:
        locations = loc_by_bbox(kwargs['sw'], kwargs['ne'], limit, offset, subquery=True)
        reviews = Reviews.query.filter(Reviews.loc_id.in_(locations))

    elif ('sw' in kwargs and not 'ne' in kwargs) or ('ne' in kwargs and not 'sw' in kwargs):
        abort(404, 'For bbox, both ne and sw params are required')

    elif 'user_id' in kwargs:
        reviews = Reviews.query.filter(
            Reviews.user_id == kwargs['user_id']).limit(limit).offset(offset).all()
    elif 'loc_id' in kwargs:
        reviews = Reviews.query.filter(
            Reviews.loc_id == kwargs['loc_id']).limit(limit).offset(offset).all()
    else:
        abort(404, 'Query parameters required')

    if reviews is not None:
        reviews_schema = ReviewsSchema(many=True)
        data = reviews_schema.dump(reviews)
        return data


def read_one(user_id, loc_id):
    """
    This function responds to a request 
    to /api/reviews/user/{user_id}/location/{loc_id}
    with one matching review based on loc and user
    :param user_id:   id of user
    :param loc_id:    id of location
    :return:          review matching user and location
    """

    review = (
        Reviews.query.filter(Reviews.loc_id == loc_id,
                             Reviews.user_id == user_id).one_or_none()
    )
    if review is not None:
        review_schema = ReviewsSchema()

        data = review_schema.dump(review)
        return data
    else:
        abort(
            404, f"Review for user {user_id} and location {loc_id} not found"
        )


def update(user_id, loc_id, body):
    """
    This function responds to a PUT request 
    to /api/reviews/user/{user_id}/location/{loc_id}.
    updating an existing review and comment for a give user/loc int he Reviews structure
    :param location_id:   Id of the location to update in the location structure
    :param user_id:      user id
    :param loc_id:       location id
    :param body:         updated comment and review
    :return:             updated review structure
    """

    update_review = (
        Reviews.query.filter(Reviews.loc_id == loc_id,
                             Reviews.user_id == user_id).one_or_none()
    )

    if update_review is not None:

        try:
            body['loc_id'] = update_review.loc_id
            body['user_id'] = update_review.user_id
            reviews_schema = ReviewsSchema()

            update = reviews_schema.load(body, session=db.session)
            update.id = update_review.id

            db.session.merge(update)
            db.session.commit()

            return body, 200
        except ValidationError as e:

            abort(400, str(e))

    else:
        abort(
            404, f"Review for user {user_id} and location {loc_id} not found"
        )


def delete(user_id, loc_id):
    """
    This function responds to a DELETE request to
    /api/reviews/user/{user_id}/location/{loc_id}
    deleting a review from the reviews structure
    :param user_id:      user id
    :param loc_id:       location id
    :return:            200 on successful delete, 404 if not found
    """
    review = (
        Reviews.query.filter(Reviews.loc_id == loc_id,
                             Reviews.user_id == user_id).one_or_none()
    )

    if review is not None:
        db.session.delete(review)
        db.session.commit()
        return make_response(
            f"successfully deleted review", 200
        )
    else:
        abort(
            404, f"Review for user {user_id} and location {loc_id} not found"
        )


def create(user_id, loc_id, body):
    """
    This function responds to a POST request 
    to /api/reviews/user/{user_id}/location/{loc_id}
    creating a new review in the review structure 
    for the user and location specified
    :param user_id:      user id
    :param loc_id:       location id
    :param body:       updated comment and revie
    :return:        201 on success, 406 on user exists
    """

    existing_review = (
        Reviews.query.filter(Reviews.loc_id == loc_id,
                             Reviews.user_id == user_id).one_or_none()
    )

    if existing_review is None:

        try:
            schema = ReviewsSchema()
            body['user_id'] = user_id
            body['loc_id'] = loc_id

            new_review = schema.load(body, session=db.session)
            db.session.add(new_review)
            db.session.commit()

            data = schema.dump(new_review)

            return data, 201
        except ValidationError as e:

            abort(400, str(e))

    else:
        abort(
            406, f"Review for user {user_id} and location {loc_id} already exists")
