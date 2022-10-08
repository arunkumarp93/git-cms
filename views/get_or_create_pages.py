from flask import Blueprint, render_template, request, session
from flask_login import login_required
from flask_login import current_user

from views.utils.github import (
    get_github_auth_token,
    get_generate_github_object,
    get_current_user_name_from_github,
    get_folder_and_repo,
)

get_page = Blueprint("get_page", __name__)


@get_page.route("/", methods=["GET"])
def get_all_pages() -> str:
    """
    i)   Validate user and repo configuration in the session
    ii)  Validate repo exist in the GitHub
         a) validate the folder inside the repo
         b) fetch all the posts inside the repo
    :return: (str) Index HTML page
    """
    context = {
        "session": current_user,
        "posts": [],
        "is_valid_token": False,
        "repo_exist": False,
        "folder_exist": False,
        "message": "",
        "exception": None,
    }
    github_token = get_github_auth_token()
    if github_token:
        # fetch the posts from the repo
        try:
            github = get_generate_github_object(github_token)
            current_username = get_current_user_name_from_github(github)

            context["is_valid_token"] = True

            repo_name, blogs_folder_name = get_folder_and_repo()

            if current_username and repo_name and blogs_folder_name:
                repo = github.get_repo(f"{current_username}/{repo_name}")
                blog_folder_content = repo.get_contents(blogs_folder_name)
                posts = [content.name for content in blog_folder_content]
                context["repo_exist"] = True
                context["folder_exist"] = True
                context["posts"] = posts
        except Exception as e:
            context["exception"] = str(e.args)
            return render_template("index.html", context=context)

    return render_template("index.html", context=context)


@get_page.route("/configure", methods=["GET", "POST"])
@login_required
def configure_folders():
    if request.method == "POST":
        configure_form = request.form
        blogs_folder_name = configure_form.get("blogs-folder-name")
        drafts_folder_name = configure_form.get("draft-folder-name")
        repo_name = configure_form.get("repo-name")
        session["blogs_folder_name"] = blogs_folder_name
        session["drafts_folder_name"] = drafts_folder_name
        session["repo_name"] = repo_name

    session["blogs_folder_name"] = session.get("blogs_folder_name", "")
    session["drafts_folder_name"] = session.get("drafts_folder_name", "")
    session["repo_name"] = session.get("repo_name", "")
    return render_template("configure_folders.html", **session)
