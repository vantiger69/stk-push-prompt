from flask import Flask 
from flask_cors import CORS
from .routes import mpesa_routes
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os 
from dotenv import load_dotenv


db = SQLAlchemy()
load_dotenv()

def create_app():
    app = Flask(__name__)

    print("Callback URL:", os.getenv("CALLBACK_URL"))




    callback_url = os.getenv("CALLBACK_URL")

    app.config["CALLBACK_URL"] = callback_url


    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://stk_user:van@localhost/stk_push_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    CORS(app)
    migrate = Migrate(app, db)


    #from . import models
    from .models import User, STKPushRequest, STKPushResponse, Transaction
    app.register_blueprint(mpesa_routes)

    return app