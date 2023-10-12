from flask import Flask
from flask_restful import Api
from app.backend.api.api_routes import RandomAddress, RandomFilipinoUser, RandomName, RandomPhoneNumber, RandomUserInfo
from app.backend.api.index import index_bp


def start_app():
    app = Flask(__name__)
    api = Api(app)

    # index blueprint
    app.register_blueprint(index_bp)

    api.add_resource(RandomFilipinoUser, '/api/random-user')
    api.add_resource(RandomAddress, '/api/random-address')
    api.add_resource(RandomName, '/api/random-name')
    api.add_resource(RandomPhoneNumber, '/api/random-phone')

    return app



    