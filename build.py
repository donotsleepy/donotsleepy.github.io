"""Build the static blog from Markdown files in content/posts/."""

from datetime import date
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).parent
POSTS = ROOT / "content" / "posts"
OUT = ROOT / "dist"


def read_post(path):
    source = path.read_text(encoding="utf-8")
    if not source.startswith("---\n"):
        raise ValueError(f"Missing front matter: {path}")
    _, metadata, body = source.split("---\n", 2)
    fields = {}
    for line in metadata.splitlines():
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip().strip('"')
    for key in ("title", "date", "category", "summary", "reading_time"):
        if not fields.get(key):
            raise ValueError(f"Missing {key}: {path}")
    fields["date_obj"] = date.fromisoformat(fields["date"])
    fields["slug"] = path.stem
    fields["body"] = body.strip()
    return fields


def markdown_to_html(source):
    """Render the simple Markdown used by the example posts."""
    blocks = []
    paragraph = []
    list_items = []

    def flush():
        nonlocal paragraph, list_items
        if paragraph:
            blocks.append("<p>" + " ".join(escape(line) for line in paragraph) + "</p>")
            paragraph = []
        if list_items:
            blocks.append("<ul>" + "".join(f"<li>{escape(item)}</li>" for item in list_items) + "</ul>")
            list_items = []

    for line in source.splitlines():
        stripped = line.strip()
        if not stripped:
            flush()
        elif stripped.startswith("## "):
            flush()
            blocks.append(f"<h2>{escape(stripped[3:])}</h2>")
        elif stripped.startswith("> "):
            flush()
            blocks.append(f"<blockquote><p>{escape(stripped[2:])}</p></blockquote>")
        elif stripped.startswith("- "):
            if paragraph:
                flush()
            list_items.append(stripped[2:])
        else:
            if list_items:
                flush()
            paragraph.append(stripped)
    flush()
    return "\n".join(blocks)


def article_html(post):
    title = escape(post["title"])
    summary = escape(post["summary"])
    category = escape(post["category"])
    day = post["date_obj"].strftime("%Y.%m.%d")
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} — 留白</title><meta name="description" content="{summary}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css"></head><body><div class="page"><header class="site-header"><a class="brand" href="/" aria-label="留白，返回首页">留白<span style="color:#bc6244">.</span></a><nav class="nav" aria-label="主导航"><a href="/#writing">文章</a><a href="/#about">关于</a></nav></header><main><article><header class="article-header reveal"><a class="back-link" href="/#writing">← 返回文章列表</a><div class="article-meta"><span>{category}</span><span class="dot"></span><time datetime="{post['date']}">{day}</time><span class="dot"></span><span>{escape(post['reading_time'])} 分钟阅读</span></div><h1>{title}</h1><p class="article-summary">{summary}</p></header><hr class="article-rule"><div class="article-body">{markdown_to_html(post['body'])}</div><div class="article-end"><a class="back-link" href="/#writing">← 所有文章</a><span>留一点空白，给下一次思考。</span></div></article></main><footer class="site-footer"><span>© 2026 留白</span><span>写作让时间留下痕迹</span></footer></div></body></html>'''


def main():
    posts = sorted((read_post(p) for p in POSTS.glob("*.md")), key=lambda p: p["date_obj"], reverse=True)
    if not posts:
        raise ValueError("Add at least one Markdown post to content/posts/")
    rows = []
    for index, post in enumerate(posts, 1):
        title = escape(post["title"])
        category = escape(post["category"])
        day = post["date_obj"].strftime("%Y.%m.%d")
        rows.append(f'<a class="post-row" href="/posts/{post["slug"]}/"><span class="post-number">{index:02d}</span><span class="post-name">{title}<small>{category} · {escape(post["reading_time"])} 分钟阅读</small></span><time class="post-date" datetime="{post["date"]}">{day}</time><span class="post-arrow" aria-hidden="true">↗</span></a>')
        directory = OUT / "posts" / post["slug"]
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "index.html").write_text(article_html(post), encoding="utf-8")

    template = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
    home = template.replace("{{post_rows}}", "".join(rows)).replace("{{post_count}}", f"01 — {len(posts):02d}")
    (OUT / "index.html").write_text(home, encoding="utf-8")
    print(f"Built {len(posts)} posts")


if __name__ == "__main__":
    main()
