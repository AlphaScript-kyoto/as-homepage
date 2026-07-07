/**
 * Portfolio data from demo-portfolio hub (for work tool)
 * Demo base URL: https://gurashiroozisan.github.io/demo-portfolio/
 */
const DEMO_PORTFOLIO_BASE = 'https://gurashiroozisan.github.io/demo-portfolio/';
const DEMO_PORTFOLIO_HUB = DEMO_PORTFOLIO_BASE + '#works';

const PORTFOLIO = [
  { type: 'tool', title: 'SyncBridge API連携', category: '業務自動化', desc: '注文・問い合わせをAPI/Webhook経由でスプレッドシートへ自動同期。', url: 'api-sync-demo/index.html', thumb: 'api-sync-demo/assets/images/preview.png', badge: 'Tool', featured: true },
  { type: 'tool', title: 'FlowBoard カンバン', category: '業務ツール', desc: 'ドラッグ&ドロップで案件ステータスを管理するカンバンボード。', url: 'kanban-demo/index.html', thumb: 'kanban-demo/assets/images/preview.png', badge: 'Tool', featured: true },
  { type: 'tool', title: 'MemberPortal 会員・決済', category: '業務ツール', desc: 'ログイン・プロフィール・注文履歴・決済UIの会員ポータル。', url: 'portal-demo/index.html', thumb: 'portal-demo/assets/images/preview.png', badge: 'Tool', featured: true },
  { type: 'tool', title: 'SalesFlow 売上集計', category: '業務自動化', desc: 'Excel・CSVの手作業集計を自動化するダッシュボード。', url: 'automation-demo/index.html', thumb: 'automation-demo/assets/images/preview.png', badge: 'Tool', featured: true },
  { type: 'tool', title: 'CRM Lite 顧客管理', category: '業務ツール', desc: '顧客情報・商談ステータス・フォロー予定を一元管理。', url: 'crm-demo/index.html', thumb: 'crm-demo/assets/images/preview.png', badge: 'Tool', featured: true },
  { type: 'lp', title: '美容室 LUMIÈRE', category: '美容・サロン', desc: 'メニュー・スタイリスト紹介・予約導線を備えた美容室LP。', url: 'salon-lp/index.html', thumb: 'salon-lp/assets/images/concept-main.jpg', badge: 'LP', featured: true },
  { type: 'lp', title: 'CAFÉ KOMOREBI', category: '飲食・カフェ', desc: 'こだわり・メニュー・空間紹介のカフェLP。', url: 'cafe-lp/index.html', thumb: 'cafe-lp/assets/images/hero.jpg', badge: 'LP', featured: true },
  { type: 'lp', title: 'TaskPilot', category: 'SaaS・アプリ', desc: 'プロジェクト管理SaaSのLP。機能・料金プラン・登録CTA。', url: 'saas-lp/index.html', thumb: 'saas-lp/assets/images/preview.png', badge: 'LP', featured: true },
  { type: 'hp', title: '株式会社ネクストブリッジ', category: 'コーポレート', desc: '5ページ構成の企業HP。サービス・実績・お問い合わせ。', url: 'corporate-hp/index.html', thumb: 'corporate-hp/assets/images/hero.jpg', badge: 'HP', featured: true },
  { type: 'hp', title: '株式会社アトラス 採用', category: '採用・リクルート', desc: '文化・募集職種・福利厚生の採用特設ページ。', url: 'recruit-lp/index.html', thumb: 'recruit-lp/assets/images/hero.jpg', badge: 'HP', featured: true },
];

function demoUrl(path) {
  return DEMO_PORTFOLIO_BASE + path;
}

function demoThumb(path) {
  return DEMO_PORTFOLIO_BASE + path;
}

function badgeClass(badge) {
  if (badge === 'Tool' || badge === 'App') return 'portfolio-badge portfolio-badge--tool';
  if (badge === 'HP') return 'portfolio-badge portfolio-badge--hp';
  return 'portfolio-badge portfolio-badge--lp';
}

function typeLabel(type) {
  if (type === 'tool') return '業務ツール';
  if (type === 'hp') return 'HP';
  return 'LP';
}

function renderPortfolioCard(item) {
  const action = item.type === 'tool' ? 'デモを試す →' : 'デモを見る →';
  return `
    <a href="${demoUrl(item.url)}" class="portfolio-card" target="_blank" rel="noopener noreferrer" data-type="${item.type}">
      <div class="portfolio-card__thumb">
        <img src="${demoThumb(item.thumb)}" alt="${item.title}" loading="lazy" width="400" height="225">
        <span class="${badgeClass(item.badge)}">${item.badge}</span>
      </div>
      <div class="portfolio-card__body">
        <span class="portfolio-card__category">${item.category}</span>
        <h2>${item.title}</h2>
        <p>${item.desc}</p>
        <span class="portfolio-card__link">${action}</span>
      </div>
    </a>`;
}

function initPortfolioPage() {
  const grid = document.getElementById('portfolioGrid');
  const filterBtns = document.querySelectorAll('[data-portfolio-filter]');
  const countEl = document.getElementById('portfolioCount');
  const statTool = document.getElementById('statTool');
  const statLp = document.getElementById('statLp');
  const statHp = document.getElementById('statHp');
  const statTotal = document.getElementById('statTotal');

  if (!grid) return;

  const TOTAL_TOOL = 22;
  const TOTAL_LP = 12;
  const TOTAL_HP = 3;
  const TOTAL_ALL = 37;

  if (statTool) statTool.textContent = TOTAL_TOOL;
  if (statLp) statLp.textContent = TOTAL_LP;
  if (statHp) statHp.textContent = TOTAL_HP;
  if (statTotal) statTotal.textContent = TOTAL_ALL;

  let currentFilter = 'all';

  function render() {
    const items = currentFilter === 'all'
      ? PORTFOLIO
      : PORTFOLIO.filter((item) => item.type === currentFilter);

    grid.innerHTML = items.map(renderPortfolioCard).join('');
    if (countEl) countEl.textContent = items.length + ' 件を表示（全' + TOTAL_ALL + '件）';
  }

  filterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      filterBtns.forEach((b) => b.classList.remove('is-active'));
      btn.classList.add('is-active');
      currentFilter = btn.dataset.portfolioFilter;
      render();
    });
  });

  render();
}

document.addEventListener('DOMContentLoaded', initPortfolioPage);
