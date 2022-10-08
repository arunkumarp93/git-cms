import re


def format_new_line(values):
    values_without_new_line = values.strip().replace("\n", "").split("-")
    return [value.strip() for value in values_without_new_line if value]


def deconstruct_post(content):
    post_content = {"title": "", "categories": "", "tags": "", "content": ""}

    title_match = re.compile(r"title: \"\s*(.*?)\"\n")
    tags_match = re.compile("(?<=tags:).*(?=---)", re.DOTALL)
    categories_match = re.compile("(?<=categories:).*(?=tags)", re.DOTALL)
    content_match = re.compile("---\n\n(.*)", re.DOTALL)

    title_content = title_match.findall(content)[0]
    blog_content = content_match.findall(content)[0]
    tags_content = tags_match.findall(content)[0]
    categories_content = categories_match.findall(content)[0]

    tags_content = format_new_line(tags_content)
    categories_content = format_new_line(categories_content)

    post_content["content"] = blog_content
    post_content["title"] = title_content
    post_content["tags"] = tags_content
    post_content["categories"] = categories_content

    return post_content
