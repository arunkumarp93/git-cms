import base64
from datetime import datetime

from flask import Blueprint, render_template, request
from flask_login import login_required

from views.utils.blog import deconstruct_post, generate_markdown
from views.utils.github import (
    get_generate_github_object,
    get_github_auth_token,
    update_or_create_file_in_posts_github,
    get_configure_repo_object,
    delete_file_from_github,
    get_folders_and_repo,
)

create_or_update = Blueprint("post_or_update", __name__, template_folder="templates")


@create_or_update.route("/create", methods=["GET", "POST"])
@login_required
def post_a_page():
    if request.method == "GET":
        return render_template("create_post.html")
    elif request.method == "POST":
        context = {}
        title, categories, tags, content, github_content = generate_markdown(
            request.form, get_sep_values=True
        )
        try:
            today_date = datetime.today().strftime("%Y-%m-%d")
            file_name = f"{today_date}-{request.form.get('filename')}.md"
            update_or_create_file_in_posts_github(github_content, file_name)
            context["message"] = "Created successfully"
        except Exception as e:
            context["error"] = f"Unable to update the blog page {str(e.args)}"

        return render_template("create_post.html", context=context)


@create_or_update.route("/create/draft", methods=["POST"])
@login_required
def post_a_draft():
    context = {}
    title, categories, tags, content, github_content = generate_markdown(
        request.form, get_sep_values=True
    )
    try:
        today_date = datetime.today().strftime("%Y-%m-%d")
        file_name = f"{today_date}-{request.form.get('filename')}.md"
        update_or_create_file_in_posts_github(
            github_content, file_name, folder="drafts"
        )
        context["message"] = "Created successfully"
    except Exception as e:
        context["error"] = f"Unable to update the blog page {str(e.args)}"
    return context


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
        return context


@create_or_update.route("/update/drafts/<string:file_name>", methods=["GET", "POST"])
@login_required
def update_or_view_draft(file_name):
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
                (
                    repo_name,
                    blogs_folder_name,
                    drafts_folder_name,
                ) = get_folders_and_repo()
                repo = get_configure_repo_object(github)
                blog_content = repo.get_contents(f"{drafts_folder_name}/{file_name}")
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
            update_or_create_file_in_posts_github(
                github_content, file_name, folder="drafts"
            )
            context["title"] = title
            context["categories"] = categories
            context["tage"] = tags
            context["content"] = content
        except Exception as e:
            context["error"] = f"Unable to update the blog page {str(e.args)}"
        return context


@create_or_update.route("/delete/<string:file_name>", methods=["delete"])
@login_required
def delete_post_file(file_name):
    return delete_file_from_github(file_name)


@create_or_update.route("/delete_draft/<string:file_name>", methods=["delete"])
@login_required
def delete_draft_file(file_name):
    return delete_file_from_github(file_name, folder="drafts")
