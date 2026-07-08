(function () {
  'use strict';

  var slides = document.querySelectorAll('.hero-showcase__slide');
  if (!slides.length) return;

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    slides.forEach(function (s, i) {
      s.classList.toggle('is-active', i === 0);
    });
    return;
  }

  var index = 0;

  function showSlide(i) {
    slides.forEach(function (slide, n) {
      slide.classList.toggle('is-active', n === i);
    });
  }

  setInterval(function () {
    index = (index + 1) % slides.length;
    showSlide(index);
  }, 3200);

  showSlide(0);
})();
