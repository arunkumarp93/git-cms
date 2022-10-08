import os
from flask import Flask
from werkzeug.routing import BaseConverter

from core.models import db, login_manager
from views import get_or_create_pages, post_or_edit_pages
from views.authentication import authenticate_page, github_blueprint

app = Flask(__name__)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def register_blueprints(flask_app):
    flask_app.register_blueprint(get_or_create_pages.get_page)
    flask_app.register_blueprint(post_or_edit_pages.create_or_update)
    flask_app.register_blueprint(authenticate_page)
    flask_app.register_blueprint(github_blueprint, url_prefix="/login")


def create_app():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./users.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.url_map.converters["regex"] = RegexConverter
    app.secret_key = "YOU-CANNOT-GUESS"

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    register_blueprints(app)

    # disable in production
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    return app
