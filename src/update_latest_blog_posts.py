"""
This script is inspired by the post "Auto-Updating Your Github Profile With Python" by Dylan Roy 
available here https://towardsdatascience.com/auto-updating-your-github-profile-with-python-cde87b638168
"""

from pathlib import Path
import datetime
import pytz
from itertools import chain
import feedparser

RSS_FEED_URL = "https://ealizadeh.com/index.xml"
NUM_POST = 7
READ_MORE_BADGE_URL = "https://img.shields.io/badge/-Read%20more%20on%20my%20blog-brightgreen?style=for-the-badge"
READ_MORE_BADGE_HTML = f'<a href="https://ealizadeh.com/blog" target="_blank"><img alt="Personal Blog" src="{READ_MORE_BADGE_URL}" /></a>'


def update_footer():
    timestamp = datetime.datetime.now(pytz.timezone("America/Montreal")).strftime("%c")
    footer = Path("./footer.md").read_text()
    return footer.format(timestamp=timestamp)


def flatten_post_tags(post_tags):
    tags = [list(item.values()) for item in post_tags]  # will generate a nested list
    return set(list(chain(*tags)))


def update_latest_blog_posts_readme(blog_feed, readme_base, join_on):
    blog_posts = blog_feed['entries']
    posts_to_add = []
    for count, post in enumerate(blog_posts):
        # remove the unnecessary 'index.html' at the end of the blog url https://ealizadeh.com/blog/abc/index.html
        post_url = post["link"].rstrip("index.html")
        post_title = post["title"]
        posts_to_add.append(f' - [{post_title}]({post_url})')

        if count == NUM_POST:
            break

    posts_joined = "\n".join(posts_to_add)
    return readme_base[:readme_base.find(rss_title)] + f"{join_on}\n{posts_joined}"


if __name__ == "__main__":
    rss_title = "## 📕 Latest Blog Posts"
    readme = Path("../README.md").read_text(encoding="utf8")

    blog_feed = feedparser.parse(RSS_FEED_URL)

    updated_readme = update_latest_blog_posts_readme(blog_feed, readme, rss_title)
    updated_readme += f"\n<space>\n \t {READ_MORE_BADGE_HTML}\n"

    with open("../README.md", "w+") as f:
        f.write(updated_readme + update_footer())
