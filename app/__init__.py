import config
from app.api import api as apis
from flask import Flask

def create_app():

    app = Flask(__name__)
    app.config.from_object(config)
    
    app.register_blueprint(apis)

    return app