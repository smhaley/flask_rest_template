import connexion
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app(config_obj=Config):

    app = connexion.App(__name__, specification_dir='./')
    app.app.config.from_object(config_obj)
    app.add_api('../swagger.yml')

    application = app.app
    db.init_app(application)
    ma.init_app(application)
    migrate.init_app(application, db)

    return app