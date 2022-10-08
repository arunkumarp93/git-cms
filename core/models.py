from dataclasses import dataclass

from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import UserMixin, LoginManager

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@dataclass
class User(UserMixin, db.Model):
    """A class that represents a user.
    Attributes
    ----------
    id: int
        The unique user identifier
    username: str
        The unique name identifying a user
    """

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(250), unique=True)


@dataclass
class OAuth(OAuthConsumerMixin, db.Model):
    """This class stores the user authentication information.
    Attributes
    ----------
    user_id: str
        The unique user identifier, same as the User.id
    user: User
        The user found in the users table
    """

    user_id: int = db.Column(db.Integer, db.ForeignKey(User.id))
    user: User = db.relationship(User)


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
