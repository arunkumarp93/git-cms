from flask import session
from flask_login import current_user
from github import Github

from core.models import OAuth


def get_github_auth_token():
    """
        Check the current user and send the token based on it
    :return:
    """
    if not current_user.is_anonymous:
        return OAuth.query.filter_by(user_id=current_user.id).first()
    return None


def get_generate_github_object(github_token):
    """

    :param github_token: OAuth GitHub token
    :return:
    """

    access_token = github_token.token
    token = access_token.get("access_token")

    return Github(token)


def get_current_user_name_from_github(github: Github):
    """

    :param github: Github object
    :return: (string) github username
    """
    logged_in_user = github.get_user()
    return logged_in_user.login


def get_folder_and_repo():
    """
    Get the repo and blogs folder data from the session
    :return: (tuple)
    """
    repo_name = session.get("repo_name")
    blogs_folder_name = session.get("blogs_folder_name")

    return repo_name, blogs_folder_name
