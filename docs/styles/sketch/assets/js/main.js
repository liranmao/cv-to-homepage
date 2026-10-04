'use strict';
const menu = document.querySelector('.menu-toggle');
const nav = document.querySelector('.topnav');
menu?.addEventListener('click', () => {
  const open = nav.classList.toggle('responsive');
  menu.setAttribute('aria-expanded', String(open));
});
document.querySelectorAll('#myLinks a').forEach(a => a.addEventListener('click', () => {
  nav.classList.remove('responsive');
  menu.setAttribute('aria-expanded', 'false');
}));

// particles.js 2.0.0. Respect the visitor's reduced-motion preference.
if (document.body.dataset.background === 'particles' && !window.matchMedia('(prefers-reduced-motion: reduce)').matches && !new URLSearchParams(location.search).has('preview')) {
    var particleColor = "#060771";
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      particleColor = "#3eb7f0";
    }
    particlesJS("particles-js", {
      "particles": {
        "number": { "value": 50, "density": { "enable": true, "value_area": 800 } },
        "color": { "value": particleColor },
        "shape": { "type": "circle", "stroke": { "width": 0, "color": "#000000" }, "polygon": { "nb_sides": 5 } },
        "opacity": { "value": 0.15, "random": false, "anim": { "enable": false } },
        "size": { "value": 3, "random": true, "anim": { "enable": false } },
        "line_linked": { "enable": true, "distance": 150, "color": particleColor, "opacity": 0.15, "width": 1 },
        "move": { "enable": true, "speed": 2, "direction": "none", "random": false, "straight": false, "out_mode": "out", "bounce": false, "attract": { "enable": false, "rotateX": 600, "rotateY": 1200 } }
      },
      "interactivity": {
        "detect_on": "window",
        "events": { "onhover": { "enable": true, "mode": "grab" }, "onclick": { "enable": true, "mode": "push" }, "resize": true },
        "modes": { "grab": { "distance": 140, "line_linked": { "opacity": 1 } }, "bubble": { "distance": 400, "size": 40, "duration": 2, "opacity": 8, "speed": 3 }, "repulse": { "distance": 200, "duration": 0.4 }, "push": { "particles_nb": 4 }, "remove": { "particles_nb": 2 } }
      },
      "retina_detect": true
    });
}
