(function () {
  'use strict';

  function initScrollTable(scrollEl) {
    var wrap = scrollEl.closest('.plan-table-wrap');
    var outer = scrollEl.closest('.plan-table-outer');
    if (!wrap || !outer) return;

    function update() {
      var maxScroll = scrollEl.scrollWidth - scrollEl.clientWidth;
      var canScroll = maxScroll > 4;

      outer.classList.toggle('is-scrollable', canScroll);

      if (!canScroll) {
        outer.classList.remove('is-scrolled', 'is-scroll-end');
        return;
      }

      outer.classList.toggle('is-scrolled', scrollEl.scrollLeft > 8);
      outer.classList.toggle('is-scroll-end', scrollEl.scrollLeft >= maxScroll - 8);
    }

    function remeasure() {
      requestAnimationFrame(function () {
        update();
        requestAnimationFrame(update);
      });
    }

    scrollEl.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', remeasure);
    window.addEventListener('load', remeasure);

    if ('ResizeObserver' in window) {
      var ro = new ResizeObserver(remeasure);
      ro.observe(scrollEl);
      ro.observe(wrap);
    }

    remeasure();
    setTimeout(remeasure, 400);
    setTimeout(remeasure, 1200);
  }

  document.querySelectorAll('.plan-table-scroll').forEach(initScrollTable);
})();
