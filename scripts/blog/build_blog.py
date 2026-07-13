#!/usr/bin/env python3
"""Build blog HTML pages, index, and sitemap entries from Markdown posts."""

from __future__ import annotations

import html
import json
import re
from datetime import date, datetime
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = ROOT / "content" / "blog"
BLOG_DIR = ROOT / "blog"
SITE_BASE = "https://alphascript-kyoto.github.io/as-homepage"
SITE_PATH = "/as-homepage"

STATIC_SITEMAP_PAGES = [
    ("/", "1.0", "monthly"),
    ("/about/", "0.8", "monthly"),
    ("/services/", "0.9", "monthly"),
    ("/works/", "0.8", "weekly"),
    ("/blog/", "0.8", "daily"),
    ("/contact/", "0.7", "monthly"),
]


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict = {}
    for line in parts[1].strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            meta[key] = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
        else:
            meta[key] = value.strip("'\"")
    return meta, parts[2].lstrip("\n")


def slug_from_filename(path: Path) -> str:
    name = path.stem
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name)


def load_posts() -> list[dict]:
    posts: list[dict] = []
    if not CONTENT_DIR.exists():
        return posts

    for path in sorted(CONTENT_DIR.glob("*.md"), reverse=True):
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        slug = meta.get("slug") or slug_from_filename(path)
        title = meta.get("title") or slug
        description = meta.get("description") or title
        date_str = str(meta.get("date") or path.stem[:10])
        try:
            post_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            post_date = date.today()

        html_body = markdown.markdown(
            body,
            extensions=["extra", "sane_lists", "smarty"],
            output_format="html5",
        )
        posts.append(
            {
                "slug": slug,
                "title": title,
                "description": description,
                "date": post_date,
                "date_iso": post_date.isoformat(),
                "date_display": f"{post_date.year}年{post_date.month}月{post_date.day}日",
                "tags": meta.get("tags") if isinstance(meta.get("tags"), list) else [],
                "body_html": html_body,
                "url": f"{SITE_PATH}/blog/{slug}/",
                "abs_url": f"{SITE_BASE}/blog/{slug}/",
                "source": path.name,
            }
        )

    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def head_block(title: str, description: str, url: str, json_ld: str = "") -> str:
    safe_title = html.escape(title)
    safe_desc = html.escape(description)
    safe_url = html.escape(url)
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{safe_title}</title>
  <meta name="description" content="{safe_desc}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Alpha Script">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:title" content="{safe_title}">
  <meta property="og:description" content="{safe_desc}">
  <meta property="og:url" content="{safe_url}">
  <meta property="og:image" content="{SITE_BASE}/assets/og-image.png">
  <meta property="og:image:width" content="1024">
  <meta property="og:image:height" content="537">
  <meta property="og:image:alt" content="Alpha Script - あなた専属のWeb運用エンジニア">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{safe_title}">
  <meta name="twitter:description" content="{safe_desc}">
  <meta name="twitter:image" content="{SITE_BASE}/assets/og-image.png">
  <link rel="icon" href="{SITE_PATH}/assets/logo.png" type="image/png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{ theme: {{ extend: {{ colors: {{ base:'#111827', accent:'#3B82F6', card:'#1F2937' }}, fontFamily:{{ sans:['Noto Sans JP','sans-serif'] }} }} }} }}
  </script>
  <link rel="stylesheet" href="{SITE_PATH}/css/polish.css">
  {json_ld}
</head>
"""


def nav_html(active: str = "blog") -> str:
    def cls(name: str) -> str:
        return "text-accent" if name == active else "text-slate-300 hover:text-accent"

    return f"""<header class="site-header sticky top-0 z-50 border-b border-slate-800 bg-base/90 backdrop-blur">
  <div class="site-container flex items-center justify-between py-2 lg:py-3">
    <a href="{SITE_PATH}/" class="site-header-brand"><img src="{SITE_PATH}/assets/logo.png" alt="Alpha Script" class="site-header-logo"></a>
    <button id="menu-btn" class="md:hidden rounded border border-slate-700 px-3 py-2 text-sm">MENU</button>
    <nav id="menu" class="hidden md:block">
      <ul class="flex items-center gap-6 text-sm font-medium">
        <li><a href="{SITE_PATH}/" class="{cls("home")}">Home</a></li>
        <li><a href="{SITE_PATH}/about/" class="{cls("about")}">About</a></li>
        <li><a href="{SITE_PATH}/services/" class="{cls("services")}">Services</a></li>
        <li><a href="{SITE_PATH}/works/" class="{cls("works")}">Works</a></li>
        <li><a href="{SITE_PATH}/blog/" class="{cls("blog")}">Blog</a></li>
        <li><a href="{SITE_PATH}/contact/" class="rounded bg-accent px-4 py-2 text-white hover:bg-blue-500">Contact</a></li>
      </ul>
    </nav>
  </div>
  <nav id="mobile-menu" class="hidden border-t border-slate-800 px-6 py-4 md:hidden">
    <ul class="space-y-3 text-sm">
      <li><a href="{SITE_PATH}/">Home</a></li>
      <li><a href="{SITE_PATH}/about/">About</a></li>
      <li><a href="{SITE_PATH}/services/">Services</a></li>
      <li><a href="{SITE_PATH}/works/">Works</a></li>
      <li><a href="{SITE_PATH}/blog/">Blog</a></li>
      <li><a href="{SITE_PATH}/contact/">Contact</a></li>
    </ul>
  </nav>
</header>
"""


def footer_scripts() -> str:
    return """<script>
  const b = document.getElementById('menu-btn');
  const m = document.getElementById('mobile-menu');
  if (b && m) b.addEventListener('click', () => m.classList.toggle('hidden'));
</script>
</body>
</html>
"""


def render_index(posts: list[dict]) -> str:
    cards = []
    for post in posts:
        tags = "".join(
            f'<span class="blog-tag">{html.escape(tag)}</span>' for tag in post["tags"][:3]
        )
        cards.append(
            f"""      <article class="blog-card">
        <p class="blog-card__date">{html.escape(post["date_display"])}</p>
        <h2 class="blog-card__title"><a href="{html.escape(post["url"])}">{html.escape(post["title"])}</a></h2>
        <p class="blog-card__desc">{html.escape(post["description"])}</p>
        <div class="blog-card__tags">{tags}</div>
      </article>"""
        )

    cards_html = "\n".join(cards) if cards else '<p class="text-slate-400">記事はまだありません。</p>'
    json_ld = f"""<script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Blog",
    "name": "Alpha Script Blog",
    "url": "{SITE_BASE}/blog/",
    "description": "Web制作・運用・業務自動化に関するコラム。"
  }}
  </script>"""

    return (
        head_block(
            "Blog | Alpha Script",
            "Web制作・運用・業務自動化に関するAlpha Scriptのコラム。",
            f"{SITE_BASE}/blog/",
            json_ld,
        )
        + "<body class=\"bg-base text-slate-100 font-sans\">\n"
        + nav_html("blog")
        + f"""<main class="site-container page-main">
  <section class="page-section">
    <p class="section-label mb-3">Blog</p>
    <h1 class="section-title mb-4">コラム</h1>
    <p class="mb-10 max-w-3xl text-slate-300">Web制作・運用改善・業務自動化について、実務に役立つ視点を発信します。</p>
    <div class="blog-list">
{cards_html}
    </div>
  </section>
</main>
"""
        + footer_scripts()
    )


def render_post(post: dict) -> str:
    tags = "".join(f'<span class="blog-tag">{html.escape(tag)}</span>' for tag in post["tags"])
    payload = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": post["description"],
        "datePublished": post["date_iso"],
        "author": {"@type": "Organization", "name": "Alpha Script"},
        "mainEntityOfPage": post["abs_url"],
        "image": f"{SITE_BASE}/assets/og-image.png",
    }
    json_ld = (
        '<script type="application/ld+json">\n  '
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + "\n  </script>"
    )

    return (
        head_block(f'{post["title"]} | Alpha Script', post["description"], post["abs_url"], json_ld)
        + "<body class=\"bg-base text-slate-100 font-sans\">\n"
        + nav_html("blog")
        + f"""<main class="site-container page-main">
  <article class="blog-article page-section">
    <p class="section-label mb-3">Blog</p>
    <p class="blog-article__date mb-3">{html.escape(post["date_display"])}</p>
    <h1 class="section-title mb-5">{html.escape(post["title"])}</h1>
    <div class="blog-card__tags mb-8">{tags}</div>
    <div class="blog-prose">
{post["body_html"]}
    </div>
    <div class="mt-12 border-t border-slate-800 pt-8">
      <a href="{SITE_PATH}/blog/" class="btn-cta btn-cta-secondary btn-cta-sm">← 記事一覧へ</a>
      <a href="{SITE_PATH}/contact/" class="btn-cta btn-cta-primary btn-cta-sm ml-3">無料相談する</a>
    </div>
  </article>
</main>
"""
        + footer_scripts()
    )


def write_sitemap(posts: list[dict]) -> None:
    today = date.today().isoformat()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, priority, freq in STATIC_SITEMAP_PAGES:
        lines.extend(
            [
                "  <url>",
                f"    <loc>{SITE_BASE}{path}</loc>",
                f"    <lastmod>{today}</lastmod>",
                f"    <changefreq>{freq}</changefreq>",
                f"    <priority>{priority}</priority>",
                "  </url>",
            ]
        )
    for post in posts:
        lines.extend(
            [
                "  <url>",
                f"    <loc>{post['abs_url']}</loc>",
                f"    <lastmod>{post['date_iso']}</lastmod>",
                "    <changefreq>monthly</changefreq>",
                "    <priority>0.6</priority>",
                "  </url>",
            ]
        )
    lines.append("</urlset>")
    lines.append("")
    (ROOT / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def clean_generated_articles(valid_slugs: set[str]) -> None:
    if not BLOG_DIR.exists():
        return
    for child in BLOG_DIR.iterdir():
        if child.name == "index.html":
            continue
        if child.is_dir() and child.name not in valid_slugs:
            for item in child.rglob("*"):
                if item.is_file():
                    item.unlink()
            for item in sorted(child.rglob("*"), reverse=True):
                if item.is_dir():
                    item.rmdir()
            child.rmdir()


def build() -> list[dict]:
    posts = load_posts()
    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    (BLOG_DIR / "index.html").write_text(render_index(posts), encoding="utf-8", newline="\n")

    for post in posts:
        article_dir = BLOG_DIR / post["slug"]
        article_dir.mkdir(parents=True, exist_ok=True)
        (article_dir / "index.html").write_text(render_post(post), encoding="utf-8", newline="\n")

    clean_generated_articles({p["slug"] for p in posts})
    write_sitemap(posts)
    return posts


if __name__ == "__main__":
    built = build()
    print(f"Built {len(built)} blog post(s).")
    for post in built:
        print(f"- {post['date_iso']} {post['slug']}")
