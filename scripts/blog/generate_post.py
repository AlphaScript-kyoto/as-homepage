#!/usr/bin/env python3
"""Generate one blog post via local LM Studio (OpenAI-compatible API)."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = ROOT / "content" / "blog"
TOPICS_PATH = Path(__file__).with_name("topics.json")

DEFAULT_BASE_URL = "http://127.0.0.1:1234/v1"

SYSTEM_PROMPT = """あなたは Alpha Script（Web運用の専属エンジニア）の公式ブログ担当です。
読者は中小企業の経営者・担当者です。専門用語は易しく、実務で使える内容にしてください。

制約:
- 日本語で書く
- 誇大広告や根拠のない断定をしない
- Alpha Script の強み（最速のプロトタイプ、待たせない運用、業務自動化）と矛盾しない
- 見出しは ## と ### のみ使う
- 800〜1200字程度
- 出力はJSONのみ（前置き・後書き禁止）
"""


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    # Prefer ASCII slug; fallback if Japanese-only
    ascii_slug = re.sub(r"[^a-z0-9-]", "", text)
    return (ascii_slug or "post")[:60]


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


def base_url() -> str:
    return os.environ.get("LM_STUDIO_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def http_json(method: str, url: str, payload: dict | None = None) -> dict:
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=180) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise SystemExit(
            "LM Studio に接続できませんでした。\n"
            f"URL: {url}\n"
            "LM Studio で Local Server を起動し、モデルを Load した状態で再実行してください。\n"
            f"詳細: {exc}"
        ) from exc


def resolve_model() -> str:
    env_model = os.environ.get("LM_STUDIO_MODEL", "").strip()
    if env_model:
        return env_model
    models = http_json("GET", f"{base_url()}/models")
    data = models.get("data") or []
    if not data:
        raise SystemExit("LM Studio に読み込み済みモデルがありません。先にモデルを Load してください。")
    return data[0]["id"]


def extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            raise
        return json.loads(match.group(0))


def chat_completion(model: str, user_prompt: str) -> str:
    payload = {
        "model": model,
        "temperature": 0.7,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    }
    result = http_json("POST", f"{base_url()}/chat/completions", payload)
    try:
        return result["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError) as exc:
        raise SystemExit(f"Unexpected LM Studio response: {result}") from exc


def generate() -> Path:
    titles = existing_titles()
    topic = pick_topic(titles)
    today = date.today().isoformat()
    model = resolve_model()

    print(f"LM Studio: {base_url()}")
    print(f"Model: {model}")
    print(f"Topic: {topic['title']}")

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

    content = chat_completion(model, user_prompt)
    data = extract_json(content)

    title = (data.get("title") or topic["title"]).strip()
    description = (data.get("description") or topic["angle"]).strip()
    slug = slugify(str(data.get("slug") or title))
    tags = data.get("tags") if isinstance(data.get("tags"), list) else topic.get("keywords", [])
    body = (data.get("body") or "").strip()

    if len(body) < 300:
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
