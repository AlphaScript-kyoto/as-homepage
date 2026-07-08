(function () {
  'use strict';

  document.querySelectorAll('.plan-table-scroll').forEach(function (scrollEl) {
    var wrap = scrollEl.closest('.plan-table-wrap');
    if (!wrap) return;

    function update() {
      var maxScroll = scrollEl.scrollWidth - scrollEl.clientWidth;

      if (maxScroll <= 4) {
        wrap.classList.add('is-scrolled', 'is-scroll-end');
        return;
      }

      if (scrollEl.scrollLeft > 8) {
        wrap.classList.add('is-scrolled');
      }

      if (scrollEl.scrollLeft >= maxScroll - 8) {
        wrap.classList.add('is-scroll-end');
      } else {
        wrap.classList.remove('is-scroll-end');
      }
    }

    scrollEl.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  });
})();
