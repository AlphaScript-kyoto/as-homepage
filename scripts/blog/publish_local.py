#!/usr/bin/env python3
"""Generate a post with LM Studio, build HTML, and print git publish steps."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(cmd: list[str]) -> None:
    print(">", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    run([sys.executable, str(ROOT / "scripts" / "blog" / "generate_post.py")])
    run([sys.executable, str(ROOT / "scripts" / "blog" / "build_blog.py")])
    print(
        "\n完了しました。公開するなら次を実行してください:\n"
        "  git add content/blog blog sitemap.xml\n"
        '  git commit -m "Publish blog post"\n'
        "  git push origin main\n"
    )


if __name__ == "__main__":
    main()
