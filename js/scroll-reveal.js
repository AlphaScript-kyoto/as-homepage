(function () {
  'use strict';

  var STAGGER_MS = 90;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function markReveal(el, delay) {
    if (el.dataset.revealInit) return;
    el.dataset.revealInit = '1';
    el.classList.add('reveal');
    if (delay > 0) {
      el.style.transitionDelay = delay + 'ms';
    }
  }

  function initStaggerGroups() {
    document.querySelectorAll('[data-reveal-stagger]').forEach(function (group) {
      var step = parseInt(group.dataset.revealStagger || String(STAGGER_MS), 10);
      var items = group.querySelectorAll('[data-reveal]');
      items.forEach(function (item, index) {
        if (!item.dataset.revealDelay) {
          item.dataset.revealDelay = String(index * step);
        }
      });
    });
  }

  function initAutoSections() {
    document.querySelectorAll('[data-reveal-auto]').forEach(function (root) {
      root.querySelectorAll('section').forEach(function (section) {
        var delay = 0;
        var step = 80;

        section.querySelectorAll('h1, h2, .section-title, .section-label').forEach(function (el) {
          el.setAttribute('data-reveal', '');
          markReveal(el, delay);
          delay += step;
        });

        section.querySelectorAll(':scope > p, :scope > div > p').forEach(function (el, i) {
          if (i > 1) return;
          if (el.closest('article, details')) return;
          el.setAttribute('data-reveal', '');
          markReveal(el, delay);
          delay += step;
        });

        section.querySelectorAll('article, details').forEach(function (el, index) {
          el.setAttribute('data-reveal', '');
          markReveal(el, index * step);
        });
      });
    });
  }

  function initManualItems() {
    document.querySelectorAll('[data-reveal]').forEach(function (el) {
      if (!el.classList.contains('reveal')) {
        var delay = parseInt(el.dataset.revealDelay || '0', 10);
        markReveal(el, delay);
      }
    });
  }

  initStaggerGroups();
  initAutoSections();
  initManualItems();

  var items = document.querySelectorAll('.reveal');
  if (!items.length) return;

  if (reduced) {
    items.forEach(function (el) {
      el.classList.add('is-visible');
    });
    return;
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    },
    {
      root: null,
      rootMargin: '0px 0px -5% 0px',
      threshold: 0.06
    }
  );

  items.forEach(function (el) {
    observer.observe(el);
  });
})();
