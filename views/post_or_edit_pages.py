import base64
from flask import Blueprint, render_template, request
from flask_login import login_required

from views.utils.blog import deconstruct_post, generate_markdown
from views.utils.github import (
    get_generate_github_object,
    get_github_auth_token,
    update_or_create_file_in_posts_github,
    get_configure_repo_object,
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

                repo, blogs_folder_name = get_configure_repo_object(
                    github, blogs_folder=True
                )
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
        title, categories, tags, content, github_content = generate_markdown(
            request.form, get_sep_values=True
        )
        try:
            update_or_create_file_in_posts_github(github_content, file_name)
            context["title"] = title
            context["categories"] = categories
            context["tage"] = tags
            context["content"] = content
        except Exception as e:
            context["error"] = f"Unable to update the blog page {str(e.args)}"
        return render_template("edit_post.html")


@create_or_update.route("/drafts", methods=["GET", "POST"])
@login_required
def list_drafts():
    return render_template("drafts.html")
