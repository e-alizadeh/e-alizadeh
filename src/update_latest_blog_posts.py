from pathlib import Path
import datetime
import pytz
from itertools import chain
import feedparser

RSS_FEED = "https://ealizadeh.com/feed"
NUM_POST = 7
READ_MORE_BADGE_URL = "https://img.shields.io/badge/-Read%20more%20on%20my%20blog-brightgreen?style=for-the-badge"
READ_MORE_BADGE_MARKDOWN = f"[![]({READ_MORE_BADGE_URL})](https://ealizadeh.com/blog)"


def update_footer():
    timestamp = datetime.datetime.now(pytz.timezone("America/Montreal")).strftime("%c")
    footer = Path("./footer.md").read_text()
    return footer.format(timestamp=timestamp)


def flatten_post_tags(post_tags):
    tags = [list(item.values()) for item in post_tags]  # will generate a nested list
    return set(list(chain(*tags)))


def update_latest_blog_posts_readme(blog_feed, readme_base, join_on):
    parsed_feed = feedparser.parse(blog_feed)
    posts = []
    for count, item in enumerate(parsed_feed.entries):
        given_tags = flatten_post_tags(item["tags"])
        if "blog" in given_tags:
            posts.append(f' - [{item["title"]}]({item["link"]})')
        if count == NUM_POST:
            break
    posts_joined = "\n".join(posts)
    return readme_base[:readme_base.find(rss_title)] + f"{join_on}\n{posts_joined}"


if __name__ == "__main__":
    rss_title = "## 📕 Latest Blog Posts"
    readme = Path("../README.md").read_text()

    updated_readme = update_latest_blog_posts_readme(RSS_FEED, readme, rss_title)
    updated_readme += f"\n<space>\n \t {READ_MORE_BADGE_MARKDOWN}\n"

    with open("../README.md", "w+") as f:
        f.write(updated_readme + update_footer())
