from flask import Flask 
from flask_cors import CORS
from .routes import mpesa_routes


def create_app():
    app = Flask(__name__)
    CORS(app)


    app.register_blueprint(mpesa_routes)

    return app