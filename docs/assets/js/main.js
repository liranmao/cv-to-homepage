'use strict';
const menu = document.querySelector('.menu-toggle');
const nav = document.querySelector('.topnav');
menu.addEventListener('click', () => {
  const open = nav.classList.toggle('responsive');
  menu.setAttribute('aria-expanded', String(open));
});
document.querySelectorAll('#myLinks a').forEach(a => a.addEventListener('click', () => {
  nav.classList.remove('responsive');
  menu.setAttribute('aria-expanded', 'false');
}));
// Small local canvas animation; no trackers or external JavaScript dependencies.
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
const dark = window.matchMedia('(prefers-color-scheme: dark)');
const canvas = document.querySelector('#particles');
const ctx = canvas.getContext('2d');
let width, height, points = [], frame;
function resize() {
  width = window.innerWidth; height = window.innerHeight;
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = width * ratio; canvas.height = height * ratio;
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  points = Array.from({length: Math.min(50, Math.ceil(width / 25))}, () => ({
    x: Math.random() * width, y: Math.random() * height,
    dx: (Math.random() - .5) * .35, dy: (Math.random() - .5) * .35
  }));
}
function draw() {
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = ctx.strokeStyle = dark.matches ? '#3eb7f0' : '#060771';
  points.forEach((p, i) => {
    p.x = (p.x + p.dx + width) % width; p.y = (p.y + p.dy + height) % height;
    ctx.globalAlpha = .15; ctx.beginPath(); ctx.arc(p.x, p.y, 2, 0, Math.PI * 2); ctx.fill();
    points.slice(i + 1).forEach(q => {
      const d = Math.hypot(p.x - q.x, p.y - q.y);
      if (d < 150) {
        ctx.globalAlpha = .12 * (1 - d / 150);
        ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke();
      }
    });
  });
  frame = requestAnimationFrame(draw);
}
function sync() {
  cancelAnimationFrame(frame);
  ctx.clearRect(0, 0, width, height);
  if (!reduced.matches && !document.hidden) draw();
}
if (ctx) {
  resize(); sync();
  window.addEventListener('resize', resize);
  reduced.addEventListener('change', sync);
  document.addEventListener('visibilitychange', sync);
}
