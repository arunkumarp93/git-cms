import datetime
import re


def format_new_line(values):
    values_without_new_line = values.strip().replace("\n", "").split("-")
    return [value.strip() for value in values_without_new_line if value]


def deconstruct_post(content):
    post_content = {"title": "", "categories": "", "tags": "", "content": ""}
    title_match = re.compile(r"title: \"\s*(.*?)\"\n")
    tags_match = re.compile("(?<=tags:).*(?=---)", re.DOTALL)
    categories_match = re.compile("(?<=categories:).*(?=tags)", re.DOTALL)
    content_match = re.compile(r"---\n\n(.*)", re.DOTALL)
    last_modified_match = re.compile(r"last_modified_at: \s*(.*?)\n")

    # carriage return must be removed
    content = content.replace("\r", "")
    title_content = title_match.findall(content)[0]
    blog_content = content_match.findall(content)[0]
    tags_content = tags_match.findall(content)[0]
    categories_content = categories_match.findall(content)[0]
    last_modified_content = last_modified_match.findall(content)
    if last_modified_content:
        last_modified_content = last_modified_content[0]
    else:
        last_modified_content = ""

    tags_content = format_new_line(tags_content)
    categories_content = format_new_line(categories_content)

    post_content["content"] = blog_content
    post_content["title"] = title_content
    post_content["tags"] = tags_content
    post_content["categories"] = categories_content
    post_content["last_modified"] = last_modified_content
    return post_content


def tags_formatter(tags):
    result = ""
    for _, tag in enumerate(tags):
        result += f"- {tag}\n  "
    # empty spaces used on markdown file to handle
    # the headers
    if not result:
        return "  "
    else:
        return result


def generate_markdown(blog_content, get_sep_values=False):
    title = blog_content.get("title")
    last_modified = datetime.datetime.utcnow().isoformat(
        sep="T", timespec="milliseconds"
    )
    categories = tags_formatter(blog_content.get("categories").split(","))
    tags = tags_formatter(blog_content.get("tags").split(","))

    content = blog_content.get("content")
    markdown = (
        f'---\ntitle: "{title}"\nlast_modified_at: {last_modified}\n'
        f"categories:\n{categories}tags:\n{tags}---\n\n{content}"
    )
    if get_sep_values:
        return title, categories, tags, content, markdown
    else:
        return markdown
