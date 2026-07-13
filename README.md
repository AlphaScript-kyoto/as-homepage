# Alpha Script

Alpha Script の公式サイト（GitHub Pages）です。  
Web制作・運用保守・業務自動化を一貫して支援する「Web運用の専属エンジニア」としての情報を掲載しています。

- 公開URL: https://alphascript-kyoto.github.io/as-homepage/
- ポートフォリオHub: https://demo-portfolio-six-mu.vercel.app/#works

## サイト構成

- `index.html` - HOME
- `about/index.html` - About
- `services/index.html` - Services
- `works/index.html` - Works
- `contact/index.html` - Contact
- `blog/` - Blog（一覧・記事。`content/blog/*.md` から生成）
- `content/blog/` - Blog原稿（Markdown）
- `scripts/blog/` - 記事生成・HTMLビルドスクリプト
- `.github/workflows/daily-blog.yml` - 毎日のAI記事生成＆公開
- `404.html` - 404ページ
- `js/main.js` - 共通UI挙動
- `js/portfolio.js` - 実績カード描画・詳細モーダル
- `llms.txt` - AI検索向け要約
- `llms-full.txt` - AI検索向け詳細
- `robots.txt` / `sitemap.xml` - クローラー向け設定

## Blog（AI自動更新）

1. 原稿は `content/blog/*.md`
2. `python scripts/blog/build_blog.py` で `blog/` と `sitemap.xml` を生成
3. GitHub の Secrets に `OPENAI_API_KEY` を入れると、毎日 9:00（JST）に記事を自動生成して push します
4. 手動実行は Actions の「Daily AI Blog」から可能です

ローカルでのビルド:

```bash
pip install -r scripts/blog/requirements.txt
python scripts/blog/build_blog.py
```

## ローカル確認

```bash
python -m http.server 8000
```

ブラウザで `http://localhost:8000/as-homepage/` を開いて確認してください。

## デプロイ

`main` ブランチを GitHub へ push すると GitHub Pages 側へ反映されます。

## SEO / AI 検索対応

- 各ページに `meta description` を設定
- JSON-LD 構造化データを配置
- `robots.txt` と `sitemap.xml` を配置
- `llms.txt` / `llms-full.txt` を配置

