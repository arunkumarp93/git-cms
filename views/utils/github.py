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


def get_folders_and_repo():
    """
    Get the repo and blogs folder data from the session
    :return: (tuple)
    """
    repo_name = session.get("repo_name")
    blogs_folder_name = session.get("blogs_folder_name")
    drafts_folder_name = session.get("drafts_folder_name")

    return repo_name, blogs_folder_name, drafts_folder_name


def get_configure_repo_object(github_object, blogs_folder=False):
    """
    Get the current repo object from github
    :param github_object:
    :param blogs_folder: (bool)
    :return:
    """
    repo_name, blogs_folder_name, drafts_folder_name = get_folders_and_repo()
    current_username = get_current_user_name_from_github(github_object)
    repo_obj = github_object.get_repo(f"{current_username}/{repo_name}")
    if not blogs_folder:
        return repo_obj
    return repo_obj, blogs_folder_name


def delete_file_from_github(filename, branch="master", folder="posts"):
    github_auth_token = get_github_auth_token()
    github_object = get_generate_github_object(github_auth_token)
    repo = get_configure_repo_object(github_object)

    _, posts, drafts = get_folders_and_repo()

    if folder == "posts":
        file_path = f"{posts}/{filename}"
    elif folder == "drafts":
        file_path = f"{drafts}/{filename}"
    else:
        file_path = ""

    posts_contents = repo.get_contents(posts)
    posts_files_name = {post.path: post.path for post in posts_contents}

    if file_path in posts_files_name:
        file_content = repo.get_contents(file_path)
        try:
            repo.delete_file(
                file_path, f"Delete {filename}", file_content.sha, branch=branch
            )
            return True
        except Exception as e:
            return {"error": f"unable to delete the file {str(e.args)}"}
    else:
        return {"error": "File does not exists"}


def update_or_create_file_in_posts_github(
    content, filename, branch="master", folder="posts"
):
    """
    i)   get the last commit hash
    ii)  create the blog content
    iii) create a tree defines the folder structure
    iv)  create the commit with the last commit
    v)   update the HEAD pointer to the current commit
    :return:

    REF:
    https://www.folkstalk.com/tech/how-to-upload-files-and-folders-with-pygithub-with-code-examples/

    """
    github_auth_token = get_github_auth_token()
    github_object = get_generate_github_object(github_auth_token)
    repo = get_configure_repo_object(github_object)

    _, posts, drafts = get_folders_and_repo()
    if folder == "posts":
        file_path = f"{posts}/{filename}"
    elif folder == "drafts":
        file_path = f"{drafts}/{filename}"
    else:
        file_path = ""
    posts_contents = repo.get_contents(posts)
    posts_files_name = {post.path: post.path for post in posts_contents}

    if file_path in posts_files_name:
        file_content = repo.get_contents(file_path)
        repo.update_file(
            file_path, f"update {filename}", content, file_content.sha, branch=branch
        )
    else:
        repo.create_file(file_path, f"create {filename}", content, branch=branch)
