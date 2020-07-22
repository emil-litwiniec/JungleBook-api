from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask
from jungle_book.auth.views import auth_bp, oauth
from jungle_book.book.views import book_bp
from jungle_book.plant.views import plant_bp

from jungle_book.user.views import user_bp

from jungle_book.fs.views import files_bp
from jungle_book.encyclopedia.views import encyclopedia_bp
from config import ProductionConfig, DevelopmentConfig
from jungle_book.db import db

from flask_cors import CORS
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__)
    if app.config['ENV'] == "production":
        app.config.from_object(ProductionConfig())
    elif app.config['ENV'] == "development":
        app.config.from_object(DevelopmentConfig())

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    setup_app(app)

    return app


def setup_app(app):
    """Create tables if they do not exist already"""
    url_prefix = "/api/"
    oauth.init_app(app)
    app.register_blueprint(auth_bp, url_prefix=url_prefix)
    app.register_blueprint(user_bp, url_prefix=url_prefix)
    app.register_blueprint(book_bp, url_prefix=url_prefix)
    app.register_blueprint(encyclopedia_bp, url_prefix=url_prefix)
    app.register_blueprint(plant_bp, url_prefix=url_prefix)
    app.register_blueprint(files_bp, url_prefix=url_prefix)
    CORS(app)


app = create_app()
db.init_app(app)
