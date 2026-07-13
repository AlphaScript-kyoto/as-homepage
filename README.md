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
- `scripts/blog/` - 記事生成・HTMLビルド（LM Studio 連携）
- `404.html` - 404ページ
- `js/main.js` - 共通UI挙動
- `js/portfolio.js` - 実績カード描画・詳細モーダル
- `llms.txt` - AI検索向け要約
- `llms-full.txt` - AI検索向け詳細
- `robots.txt` / `sitemap.xml` - クローラー向け設定

## Blog（LM Studio・API課金なし）

有料APIは使いません。ローカルの LM Studio で記事を生成します。

1. LM Studio でモデルを Load
2. **Local Server** を起動（既定: `http://127.0.0.1:1234`）
3. 次を実行:

```bash
python -m pip install -r scripts/blog/requirements.txt
python scripts/blog/publish_local.py
```

4. 内容を確認したら push:

```bash
git add content/blog blog sitemap.xml
git commit -m "Publish blog post"
git push origin main
```

任意の環境変数:

- `LM_STUDIO_BASE_URL`（既定: `http://127.0.0.1:1234/v1`）
- `LM_STUDIO_MODEL`（未指定なら読み込み済みの先頭モデル）

HTMLだけ再生成する場合:

```bash
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

