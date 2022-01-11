from flask_apiblueprint import APIBlueprint

api = APIBlueprint('api', __name__)

from . import urls