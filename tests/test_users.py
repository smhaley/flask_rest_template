from .conftest import test_client, init_database
from models import Users
from users.users_schema import UsersSchema
from uuid import uuid4
from app import db


def test_read_all(test_client, init_database):

    users = Users.query.all()
    users_schema = UsersSchema(many=True)
    data = users_schema.dump(users)

    response = test_client.get('/api/users')

    for user in data:
        assert user['email'].encode(
            'utf-8') and user['name'].encode('utf-8') in response.data

def test_read_all_offset(test_client, init_database):

    user = (
        Users.query.filter(Users.id == 3).one_or_none()
    )
    users_schema = UsersSchema()
    data = users_schema.dump(user)


    response = test_client.get('/api/users?offset=2&limit=1')
    print(response.data)

    assert data['email'].encode(
    'utf-8') and data['name'].encode('utf-8') in response.data



def test_read_one(test_client, init_database):

    user = (
        Users.query.filter(Users.id == 1).one_or_none()
    )
    users_schema = UsersSchema()
    data = users_schema.dump(user)

    response = test_client.get('/api/users/1')
    assert data['email'].encode(
        'utf-8') and data['name'].encode('utf-8') in response.data


def test_update(test_client, init_database):
    users_schema = UsersSchema()
    new_name = str(uuid4())

    user = (
        Users.query.filter(Users.id == 1).one_or_none()
    )

    data_original = users_schema.dump(user)

    post_template = {
        "email": data_original['email'],
        "name": data_original['name']
    }

    update = post_template
    update['name'] = new_name

    response = test_client.put('/api/users/1', json=update)

    updated_user = (
        Users.query.filter(Users.id == 1).one_or_none()
    )

    data_new = users_schema.dump(updated_user)

    assert new_name == data_new['name']


def test_create(test_client, init_database):
    users_schema = UsersSchema()
    new_name = str(uuid4())

    post_template = {
        "email": f'{new_name}@{new_name}.com',
        "name": new_name
    }

    response = test_client.post('/api/users', json=post_template)

    new_user = (
        Users.query.filter(Users.name == new_name).one_or_none()
    )
    data_new = users_schema.dump(new_user)

    assert data_new['name'] == post_template['name']
    assert data_new['email'] == post_template['email']


def test_create_bad_em(test_client, init_database):
    users_schema = UsersSchema()
    new_name = str(uuid4())

    post_template = {
        "email": new_name,
        "name": new_name
    }

    response = test_client.post('/api/users', json=post_template)

    new_user = (
        Users.query.filter(Users.name == new_name).one_or_none()
    )

    assert new_user is None


def test_delete(test_client, init_database):

    response = test_client.delete(f'/api/users/1')

    user_confirm = (
        Users.query.filter(Users.id == 1).one_or_none()
    )

    assert user_confirm is None
