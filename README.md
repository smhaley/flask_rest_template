## Flask REST API Example using OAS3

### Stack

- Connexion OAS3
- Marshmallow
- SQLAlchemy
- postgres
- pytest

### To initialize:

- get image: `docker pull postgres`
- run image: `docker run --name postgres-db -e POSTGRES_PASSWORD=docker -p 5432:5432 -d POSTGRES_DB=picnic postgres`
- to enter container: `docker exec -it my-postgresdb-container bash`

## Install and Migrate

- Init: `Flask db init`
- Migrate: `Flask db migrate`
- Upgrade: `Flask db upgrade`

## Get demo data

- run: `python populate_db.py`
  - Each run will dump more data into the db.

## Run

- confirm `.env` is correct
- `Flask run`
- Visit the api gui at: `http://localhost:5000/api/ui/`
