from config import ProductionConfig, StagingConfig, TestingConfig, DevelopmentConfig
from app import create_app
import models
from os.path import join, dirname
from os import environ
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

config = environ.get('CONFIG')

if config == 'prod':
    configuration = ProductionConfig
elif config == 'staging':
    configuration = StagingConfig
elif config == 'testing':
    configuration = TestingConfig
else:
    configuration = DevelopmentConfig


app = create_app(configuration).app
app.run(host='0.0.0.0', port=5000, debug=True)
