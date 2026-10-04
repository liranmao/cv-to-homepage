/* Procedural backgrounds; no network requests or framework dependencies. */
(() => {
  const host = document.getElementById('site-background');
  if (!host) return;
  const effect = document.body.dataset.background;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const preview = new URLSearchParams(location.search).has('preview');
  if (preview) document.body.classList.add('preview-static');
  const moving = () => !reduced.matches && !preview && !document.hidden && !document.body.classList.contains('motion-paused');
  if (effect === 'spotlight') {
    window.addEventListener('pointermove', e => {
      if (!moving()) return;
      host.style.setProperty('--pointer-x', e.clientX + 'px');
      host.style.setProperty('--pointer-y', e.clientY + 'px');
    }, {passive:true});
  }
  if (effect === 'particles' && preview) {
    const ns='http://www.w3.org/2000/svg';
    const svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox','0 0 1200 800');svg.setAttribute('width','100%');svg.setAttribute('height','100%');svg.style.opacity='.15';
    let seed=793;
    const random=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
    const pts=Array.from({length:50},()=>({x:random()*1200,y:random()*800}));
    pts.forEach((p,i)=>{
      const circle=document.createElementNS(ns,'circle');circle.setAttribute('cx',p.x);circle.setAttribute('cy',p.y);circle.setAttribute('r','3');circle.setAttribute('fill','currentColor');svg.append(circle);
      pts.slice(i+1).filter(q=>Math.hypot(q.x-p.x,q.y-p.y)<200).forEach(q=>{const line=document.createElementNS(ns,'line');for(const [k,v] of Object.entries({x1:p.x,y1:p.y,x2:q.x,y2:q.y,stroke:'currentColor'}))line.setAttribute(k,v);svg.append(line);});
    });host.append(svg);
  }
  if (effect === 'contours') {
    const ns = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(ns,'svg');
    svg.setAttribute('viewBox','0 0 1200 900'); svg.setAttribute('preserveAspectRatio','xMidYMid slice');
    for (let i=0;i<28;i++) {
      const p = document.createElementNS(ns,'path');
      const y=i*35-130;
      p.setAttribute('d',`M-100 ${y} C200 ${y-160} 300 ${y+220} 570 ${y+90} S930 ${y-120} 1330 ${y+260}`);
      p.setAttribute('fill','none'); p.setAttribute('stroke','currentColor'); p.setAttribute('stroke-width','1');
      svg.append(p);
    }
    host.append(svg);
  }
  if (!['stars','lines'].includes(effect)) return;
  const canvas = document.createElement('canvas'); host.append(canvas);
  const ctx=canvas.getContext('2d'); if (!ctx) return;
  let width=0,height=0,frame=0,phase=0,previous=0;
  let seed=317;
  const random=() => {seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
  const stars=Array.from({length:65},()=>({x:random(),y:random(),r:.4+random()*1.3}));
  function resize() {
    width=host.clientWidth; height=host.clientHeight;
    const dpr=Math.min(devicePixelRatio||1,2);
    canvas.width=width*dpr; canvas.height=height*dpr; ctx.setTransform(dpr,0,0,dpr,0,0);
    draw(0);
  }
  function draw(dt) {
    phase+=dt*.00016;
    ctx.clearRect(0,0,width,height);
    ctx.strokeStyle=ctx.fillStyle=getComputedStyle(host).color;
    if (effect==='stars') {
      ctx.globalAlpha=.35;
      for (const s of stars) {ctx.beginPath();ctx.arc((s.x*width+phase*45)%Math.max(width,1),s.y*height,s.r,0,Math.PI*2);ctx.fill();}
    } else {
      ctx.globalAlpha=.13;ctx.lineWidth=1;
      for (let i=0;i<18;i++) {
        ctx.beginPath();
        for (let x=0;x<=width+12;x+=12) {const y=height*(i+.5)/18+Math.sin(x/210+phase+i*.24)*28; if(x===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}
        ctx.stroke();
      }
    }
  }
  function tick(now) {const dt=previous?Math.min(now-previous,50):0;previous=now;draw(dt);frame=requestAnimationFrame(tick);}
  function sync() {cancelAnimationFrame(frame);previous=0;if(moving())frame=requestAnimationFrame(tick);else draw(0);}
  resize();sync();
  window.addEventListener('resize',resize);
  document.addEventListener('visibilitychange',sync);
  document.addEventListener('motionchange',sync);
  reduced.addEventListener('change',sync);
})();
