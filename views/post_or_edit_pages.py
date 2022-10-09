import base64
from flask import Blueprint, render_template, request
from flask_login import login_required

from views.utils.blog import deconstruct_post  # , generate_markdown
from views.utils.github import (
    get_generate_github_object,
    get_current_user_name_from_github,
    get_github_auth_token,
    get_folder_and_repo,
)

create_or_update = Blueprint("post_or_update", __name__, template_folder="templates")


@create_or_update.route("/create", methods=["GET", "POST"])
@login_required
def post_a_page():
    return render_template("create_post.html")


@create_or_update.route("/update/<string:file_name>", methods=["GET", "POST"])
@login_required
def update_or_view_page(file_name):
    context = {
        "file_exist": False,
        "file_name": "",
        "content": "",
        "error": "",
    }
    if request.method == "GET":
        if file_name:
            try:
                github_token = get_github_auth_token()
                github = get_generate_github_object(github_token)
                current_username = get_current_user_name_from_github(github)
                repo_name, blogs_folder_name = get_folder_and_repo()
                repo = github.get_repo(f"{current_username}/{repo_name}")

                blog_content = repo.get_contents(f"{blogs_folder_name}/{file_name}")
                context["file_exist"] = True
                context["content"] = deconstruct_post(
                    base64.b64decode(blog_content.raw_data["content"]).decode()
                )
                context["file_name"] = str(blog_content.name)
            except Exception as e:
                context["error"] = str(e.args)

        return render_template("edit_post.html", context=context)
    elif request.method == "POST":
        # github_content = generate_markdown(request.form)
        return render_template("edit_post.html", context=context)


@create_or_update.route("/drafts", methods=["GET", "POST"])
@login_required
def list_drafts():
    return render_template("drafts.html")
