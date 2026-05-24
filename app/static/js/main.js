/* ===========================================
   LJ DOCES — main.js
   Custom cursor · scroll reveal · nav state
   =========================================== */

(() => {
  const fine = window.matchMedia('(pointer: fine)').matches;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── Custom cursor (desktop only) ── */
  if (fine && !reduced) {
    const dot  = document.createElement('div');
    const ring = document.createElement('div');
    dot.className  = 'cursor-dot';
    ring.className = 'cursor-ring';
    document.body.appendChild(dot);
    document.body.appendChild(ring);

    let mx = window.innerWidth / 2, my = window.innerHeight / 2;
    let rx = mx, ry = my;

    document.addEventListener('mousemove', e => {
      mx = e.clientX; my = e.clientY;
      dot.style.transform = `translate(${mx}px, ${my}px) translate(-50%, -50%)`;
    });

    const tick = () => {
      rx += (mx - rx) * 0.18;
      ry += (my - ry) * 0.18;
      ring.style.transform = `translate(${rx}px, ${ry}px) translate(-50%, -50%)`;
      requestAnimationFrame(tick);
    };
    tick();

    const hoverables = 'a, button, [data-cursor], input, textarea, select, label';
    document.querySelectorAll(hoverables).forEach(el => {
      el.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'));
      el.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'));
    });

    document.addEventListener('mouseleave', () => { dot.style.opacity = '0'; ring.style.opacity = '0'; });
    document.addEventListener('mouseenter', () => { dot.style.opacity = '';  ring.style.opacity = ''; });
  }

  /* ── Nav scrolled state ── */
  const nav = document.querySelector('.nav');
  if (nav) {
    const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 24);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ── Scroll reveal (IntersectionObserver) ── */
  const targets = document.querySelectorAll('[data-reveal]');
  if (targets.length) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('in-view');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -10% 0px' });
    targets.forEach(el => io.observe(el));
  }

  /* ── Form: floating labels (toggle has-value) ── */
  document.querySelectorAll('.field input, .field textarea, .field select').forEach(el => {
    const sync = () => el.classList.toggle('has-value', el.value && el.value.length > 0);
    sync();
    el.addEventListener('input', sync);
    el.addEventListener('change', sync);
  });

  /* ── Year footer ── */
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
