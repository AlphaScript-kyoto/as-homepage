#!/usr/bin/env python3
"""Generate one blog post with OpenAI and save it as Markdown."""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = ROOT / "content" / "blog"
TOPICS_PATH = Path(__file__).with_name("topics.json")

SYSTEM_PROMPT = """あなたは Alpha Script（Web運用の専属エンジニア）の公式ブログ担当です。
読者は中小企業の経営者・担当者です。専門用語は易しく、実務で使える内容にしてください。

制約:
- 日本語で書く
- 誇大広告や根拠のない断定をしない
- Alpha Script の強み（最速のプロトタイプ、待たせない運用、業務自動化）と矛盾しない
- Markdown本文のみ（タイトルや説明はJSON側で返す）
- 見出しは ## と ### のみ使う
- 800〜1200字程度
"""


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:60] or "post"


def existing_titles() -> set[str]:
    titles: set[str] = set()
    if not CONTENT_DIR.exists():
        return titles
    for path in CONTENT_DIR.glob("*.md"):
        for line in path.read_text(encoding="utf-8").splitlines()[:20]:
            if line.startswith("title:"):
                titles.add(line.split(":", 1)[1].strip().strip("'\""))
                break
    return titles


def pick_topic(titles: set[str]) -> dict:
    topics = json.loads(TOPICS_PATH.read_text(encoding="utf-8"))
    for topic in topics:
        if topic["title"] not in titles:
            return topic
    # fallback: reuse with date suffix idea
    return topics[date.today().toordinal() % len(topics)]


def build_markdown(meta: dict, body: str) -> str:
    tags = meta.get("tags") or ["Web運用"]
    tag_str = "[" + ", ".join(tags) + "]"
    return (
        "---\n"
        f"title: {meta['title']}\n"
        f"description: {meta['description']}\n"
        f"date: {meta['date']}\n"
        f"tags: {tag_str}\n"
        "---\n\n"
        f"{body.strip()}\n"
    )


def generate() -> Path:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("OPENAI_API_KEY is not set. Skipping generation.")
        sys.exit(0)

    from openai import OpenAI

    titles = existing_titles()
    topic = pick_topic(titles)
    today = date.today().isoformat()

    client = OpenAI(api_key=api_key)
    user_prompt = f"""次のテーマでブログ記事を書いてください。

テーマ: {topic['title']}
狙い: {topic['angle']}
キーワード: {', '.join(topic.get('keywords', []))}

出力は必ず次のJSONだけにしてください:
{{
  "title": "記事タイトル",
  "description": "120字以内の説明文",
  "slug": "english-kebab-case-slug",
  "tags": ["タグ1", "タグ2"],
  "body": "Markdown本文"
}}
"""

    response = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.7,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = response.choices[0].message.content or "{}"
    data = json.loads(content)

    title = (data.get("title") or topic["title"]).strip()
    description = (data.get("description") or topic["angle"]).strip()
    slug = slugify(data.get("slug") or title)
    tags = data.get("tags") if isinstance(data.get("tags"), list) else topic.get("keywords", [])
    body = (data.get("body") or "").strip()

    if len(body) < 400:
        raise SystemExit(f"Generated body too short ({len(body)} chars). Aborting.")

    if title in titles:
        print(f"Title already exists: {title}. Skipping.")
        sys.exit(0)

    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CONTENT_DIR / f"{today}-{slug}.md"
    if out_path.exists():
        out_path = CONTENT_DIR / f"{today}-{slug}-2.md"

    markdown_text = build_markdown(
        {
            "title": title,
            "description": description,
            "date": today,
            "tags": tags[:4],
        },
        body,
    )
    out_path.write_text(markdown_text, encoding="utf-8", newline="\n")
    print(f"Generated: {out_path.relative_to(ROOT)}")
    return out_path


if __name__ == "__main__":
    generate()
