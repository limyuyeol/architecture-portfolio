'use strict';

// Static HTML remains readable without JavaScript. JS only enhances the gallery.
(() => {
  const dialog = document.querySelector('.lightbox');
  if (!dialog) return;
  const buttons = [...document.querySelectorAll('.gallery-button')];
  const image = dialog.querySelector('#lightbox-image');
  const caption = dialog.querySelector('#lightbox-caption');
  const counter = dialog.querySelector('#lightbox-counter');
  const original = dialog.querySelector('#lightbox-original');
  let activeIndex = 0;
  let trigger = null;

  function showImage(index) {
    activeIndex = (index + buttons.length) % buttons.length;
    const button = buttons[activeIndex];
    image.src = button.dataset.image;
    image.alt = button.dataset.caption;
    caption.textContent = button.dataset.caption;
    counter.textContent = `${String(activeIndex + 1).padStart(2, '0')} / ${String(buttons.length).padStart(2, '0')}`;
    original.href = button.dataset.image;
  }

  buttons.forEach((button, index) => {
    button.addEventListener('click', () => {
      trigger = button;
      showImage(index);
      if (!dialog.open) dialog.showModal();
      document.body.classList.add('has-lightbox');
    });
  });
  dialog.querySelector('.lightbox-close').addEventListener('click', () => dialog.close());
  dialog.querySelector('.lightbox-prev').addEventListener('click', () => showImage(activeIndex - 1));
  dialog.querySelector('.lightbox-next').addEventListener('click', () => showImage(activeIndex + 1));
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); showImage(activeIndex - 1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); showImage(activeIndex + 1); }
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('has-lightbox');
    trigger?.focus({ preventScroll: true });
  });
  dialog.addEventListener('click', event => {
    if (event.target === dialog) dialog.close();
  });
})();
