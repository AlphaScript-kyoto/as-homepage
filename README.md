# Alpha Script

HP制作・LP制作・業務改善ツール開発を行うWeb制作会社の公式ウェブサイトです。

**公開URL（GitHub Pages）:** https://gurashiroozisan.github.io/alpha-script-kyoto/

## サイト構成

```
├── index.html          # トップページ
├── about/              # 会社について
├── services/           # サービス・FAQ
├── works/              # 制作実績
├── contact/            # お問い合わせ
├── css/style.css       # スタイルシート
├── js/main.js          # ナビゲーション等
├── assets/             # 画像・アイコン
├── robots.txt          # 検索エンジン・AIクローラー設定
├── llms.txt            # AI検索向けサイト概要
├── llms-full.txt       # AI検索向け詳細コンテンツ
└── sitemap.xml         # サイトマップ
```

## GitHub Pages 公開手順

### 1. リポジトリにプッシュ

```bash
git init
git add .
git commit -m "Initial commit: Alpha Script Kyoto website"
git branch -M main
git remote add origin https://github.com/gurashiroozisan/alpha-script-kyoto.git
git push -u origin main
```

### 2. GitHub Pages を有効化

1. GitHub のリポジトリページを開く
2. **Settings** → **Pages**
3. **Source** で `Deploy from a branch` を選択
4. **Branch** で `main` / `/ (root)` を選択
5. **Save** をクリック

数分後、 https://gurashiroozisan.github.io/alpha-script-kyoto/ で公開されます。

### 3. カスタムドメイン（任意）

独自ドメインを使う場合:

1. リポジトリ直下に `CNAME` ファイルを作成し、ドメイン名を記述
2. DNS で CNAME レコードを `gurashiroozisan.github.io` に向ける
3. GitHub Pages 設定でカスタムドメインを入力
4. 全 HTML 内の URL を新ドメインに差し替え（`sitemap.xml`, `llms.txt`, `robots.txt`, canonical タグ等）

## 公開前に差し替える項目

- [ ] `contact/index.html` のメールアドレス（`contact@example.com`）
- [ ] お問い合わせフォーム（Formspree 等の設定、またはフォーム削除）
- [ ] `works/` の制作実績（現在はサンプル）
- [ ] サービス内容・理念が実際の事業と合っているか確認
- [ ] OGP 画像を PNG（1200×630）に変換すると SNS 共有時の互換性が向上

## SEO・AI検索対策

本サイトには以下の対策を実装済みです:

| 対策 | ファイル/実装 |
|------|--------------|
| メタタグ・OGP | 各 HTML の `<head>` |
| 構造化データ (JSON-LD) | Organization, Service, FAQ, BreadcrumbList |
| サイトマップ | `sitemap.xml` |
| robots.txt | AI クローラー（GPTBot, ClaudeBot, PerplexityBot 等）を許可 |
| llms.txt | AI エージェント向けサイト概要 |
| llms-full.txt | AI 向け詳細コンテンツ |
| セマンティック HTML | `<main>`, `<article>`, `<nav>`, ARIA 属性 |
| data-ai-summary | 各ページ冒頭の要約文（AI 引用向け） |

### Google Search Console 登録（推奨）

公開後、 [Google Search Console](https://search.google.com/search-console) にサイトを登録し、`sitemap.xml` を送信してください。

### Bing Webmaster Tools（推奨）

[Bing Webmaster Tools](https://www.bing.com/webmasters) にも登録すると、Copilot 等でのインデックスに役立ちます。

## ローカルプレビュー

```bash
# Python が入っている場合
python -m http.server 8000
# http://localhost:8000/alpha-script-kyoto/ で確認
# ※ GitHub Pages と同じパス構造のため、ルートではなく /alpha-script-kyoto/ でアクセス
```

## ライセンス

© 2026 Alpha Script. All rights reserved.
