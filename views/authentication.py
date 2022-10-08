from flask import Blueprint, url_for, redirect, session
from flask_dance.contrib.github import github, make_github_blueprint
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_login import logout_user, login_required, login_user
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound

from core.models import OAuth, db, User

authenticate_page = Blueprint("authenticate_page", __name__)

client_id = "0559e533f3f472d0ab3a"
client_secret = "37ee85ab5e65b0c614c0d2455d5ea499e74db3c2"
github_identity_url = "https://github.com/login/oauth/authorize"
github_access_token_url = "https://github.com/login/oauth/access_token"


@authenticate_page.route("/github")
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    return redirect(url_for("get_page.get_all_pages"))


@authenticate_page.route("/logout")
@login_required
def logout():
    logout_user()
    # TODO: revoke the current token
    session.pop("blogs_folder_name")
    session.pop("drafts_folder_name")
    session.pop("repo_name")
    return redirect(url_for("get_page.get_all_pages"))


github_blueprint = make_github_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    redirect_url="http://localhost:5000",
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user,
        user_required=False,
    ),
)


@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint, token):
    info = github.get("/user")
    if info.ok:
        account_info = info.json()
        username = account_info["login"]

        query = User.query.filter_by(username=username)
        try:
            user = query.one()
        except NoResultFound:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        login_user(user)
