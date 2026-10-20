const DEMO_PORTFOLIO_BASE = 'https://demo-portfolio-six-mu.vercel.app/';
const PORTFOLIO = [
  { type: 'tool', title: 'SyncBridge API連携', category: '業務自動化', desc: '注文・問い合わせをAPI/Webhook経由で自動同期。', story: '課題: 複数チャネルの受注情報を手入力で転記し、更新漏れが発生。解決: API連携で受注データを一元化し、通知まで自動化。結果: 転記工数を削減し、確認待ちの時間を大幅に短縮。', url: 'api-sync-demo/index.html', thumb: 'api-sync-demo/assets/images/preview.png', badge: 'Tool' },
  { type: 'tool', title: 'FlowBoard カンバン', category: '業務ツール', desc: 'ドラッグ操作で案件ステータスを管理。', story: '課題: 案件の進捗が口頭・チャット依存で、担当者の把握にタイムラグ。解決: カンバンで進捗をリアルタイム可視化。結果: 確認のやり取りが減り、意思決定が速くなった。', url: 'kanban-demo/index.html', thumb: 'kanban-demo/assets/images/preview.png', badge: 'Tool' },
  { type: 'tool', title: 'CRM Lite 顧客管理', category: '業務ツール', desc: '顧客情報と商談状況を一元管理。', story: '課題: 顧客情報が複数ファイルに散在し、引き継ぎ時に情報欠落。解決: 顧客情報と商談履歴を一画面に統合。結果: 担当交代時も対応品質を保ち、返信待ちを抑制。', url: 'crm-demo/index.html', thumb: 'crm-demo/assets/images/preview.png', badge: 'Tool' },
  { type: 'tool', title: 'SalesFlow 売上集計', category: '業務自動化', desc: 'Excel/CSV集計を自動化するダッシュボード。', story: '課題: 月次集計が手作業で、レポート作成まで数日を要していた。解決: CSV取り込みから集計までを自動処理。結果: 数値把握を当日化し、改善施策の着手が前倒しに。', url: 'automation-demo/index.html', thumb: 'automation-demo/assets/images/preview.png', badge: 'Tool' },
  { type: 'lp', title: '美容室 LUMIÈRE', category: '美容・サロン', desc: '予約導線付き美容室LP。', story: '課題: SNS流入はあるが予約につながらない。解決: ファーストビューで訴求を整理し、予約導線を最短化。結果: 訪問から予約までの離脱を減らし、反応率を改善。', url: 'salon-lp/index.html', thumb: 'salon-lp/assets/images/concept-main.jpg', badge: 'LP' },
  { type: 'lp', title: 'CAFÉ KOMOREBI', category: '飲食・カフェ', desc: 'こだわり訴求のカフェLP。', story: '課題: 店舗の魅力が伝わらず、新規来店が伸び悩み。解決: ストーリー設計と写真配置で世界観を再構築。結果: 情報理解が早まり、来店検討の後押しに成功。', url: 'cafe-lp/index.html', thumb: 'cafe-lp/assets/images/hero.jpg', badge: 'LP' },
  { type: 'lp', title: 'TaskPilot', category: 'SaaS・アプリ', desc: 'SaaS向けプロダクトLP。', story: '課題: 機能説明が先行し、導入メリットが伝わりづらい。解決: 課題起点の導線へ再設計し、比較・料金セクションを最適化。結果: 問い合わせ前の理解度が向上し、商談化率が改善。', url: 'saas-lp/index.html', thumb: 'saas-lp/assets/images/preview.png', badge: 'LP' },
  { type: 'hp', title: '株式会社ネクストブリッジ', category: 'コーポレート', desc: 'コーポレートHPデモ。', story: '課題: 会社情報が整理されておらず、信頼形成に時間がかかる。解決: 事業内容・実績・導線を明確に再設計。結果: 初回閲覧時の理解が深まり、問い合わせ導線が機能。', url: 'corporate-hp/index.html', thumb: 'corporate-hp/assets/images/hero.jpg', badge: 'HP' },
  { type: 'hp', title: '株式会社アトラス 採用', category: '採用・リクルート', desc: '採用サイトデモ。', story: '課題: 求人情報だけでは応募動機が形成されにくい。解決: 働く環境と価値観を伝える構成に変更。結果: 応募前の不安を減らし、エントリー行動を促進。', url: 'recruit-lp/index.html', thumb: 'recruit-lp/assets/images/hero.jpg', badge: 'HP' },
  { type: 'tool', title: 'MemberPortal 会員・決済', category: '業務ツール', desc: '会員情報・注文履歴・決済UI。', story: '課題: 会員対応と決済確認が分断され、問い合わせ対応が遅延。解決: 会員情報・履歴・決済状態を一元表示。結果: サポート対応時間を短縮し、顧客待ちを削減。', url: 'portal-demo/index.html', thumb: 'portal-demo/assets/images/preview.png', badge: 'Tool' }
];

function card(item) {
  const href = DEMO_PORTFOLIO_BASE + item.url;
  const img = DEMO_PORTFOLIO_BASE + item.thumb;
  return `
  <article class="group overflow-hidden rounded-xl border border-slate-800 bg-card transition hover:-translate-y-1 hover:border-accent">
    <img src="${img}" alt="${item.title}" class="h-44 w-full object-cover" onerror="this.src='/assets/logo.png';this.style.objectFit='contain';this.style.padding='1rem';">
    <div class="p-4">
      <span class="text-xs font-semibold text-accent">${item.category}</span>
      <h3 class="mt-1 text-lg font-bold text-slate-100">${item.title}</h3>
      <p class="mt-2 text-sm text-slate-300">${item.desc}</p>
      <div class="mt-4 flex gap-2">
        <a href="${href}" target="_blank" rel="noopener noreferrer" class="rounded bg-accent px-3 py-2 text-xs font-semibold text-white">デモを開く</a>
        <button type="button" class="rounded border border-slate-600 px-3 py-2 text-xs font-semibold text-slate-200 hover:border-accent hover:text-accent" data-story-open data-title="${item.title}" data-category="${item.category}" data-desc="${item.desc}" data-story="${item.story || ''}" data-url="${href}">課題解決ストーリー</button>
      </div>
    </div>
  </article>`;
}

document.addEventListener('DOMContentLoaded', () => {
  const grid = document.getElementById('portfolioGrid');
  const count = document.getElementById('portfolioCount');
  const btns = document.querySelectorAll('[data-portfolio-filter]');
  const modal = document.getElementById('storyModal');
  const modalTitle = document.getElementById('storyModalTitle');
  const modalCategory = document.getElementById('storyModalCategory');
  const modalDesc = document.getElementById('storyModalDesc');
  const modalStory = document.getElementById('storyModalStory');
  const modalLink = document.getElementById('storyModalLink');
  const modalClose = document.getElementById('storyModalClose');
  if (!grid) return;

  const render = (type='all') => {
    const items = type === 'all' ? PORTFOLIO : PORTFOLIO.filter(x => x.type === type);
    grid.innerHTML = items.map(card).join('');
    if (count) count.textContent = `${items.length} 件を表示（全37件）`;

    if (modal) {
      grid.querySelectorAll('[data-story-open]').forEach((btn) => {
        btn.addEventListener('click', () => {
          modalCategory.textContent = btn.dataset.category || '';
          modalTitle.textContent = btn.dataset.title || '';
          modalDesc.textContent = btn.dataset.desc || '';
          modalStory.textContent = btn.dataset.story || '課題解決ストーリーは準備中です。';
          modalLink.href = btn.dataset.url || '#';
          modal.showModal();
        });
      });
    }
  };

  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      btns.forEach(b => b.classList.remove('bg-accent','text-white'));
      btn.classList.add('bg-accent','text-white');
      render(btn.dataset.portfolioFilter);
    });
  });

  render('all');

  if (modal && modalClose) {
    modalClose.addEventListener('click', () => modal.close());
    modal.addEventListener('click', (event) => {
      const dialogRect = modal.getBoundingClientRect();
      const insideDialog =
        event.clientX >= dialogRect.left &&
        event.clientX <= dialogRect.right &&
        event.clientY >= dialogRect.top &&
        event.clientY <= dialogRect.bottom;
      if (!insideDialog) modal.close();
    });
  }
});

