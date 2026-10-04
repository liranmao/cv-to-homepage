/* Procedural backgrounds: one Canvas loop at most; decoration never blocks content. */
(() => {
  const host = document.getElementById('site-background');
  if (!host) return;
  const effect = document.body.dataset.background;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const preview = new URLSearchParams(location.search).has('preview');
  if (preview) document.body.classList.add('preview-static');
  const moving = () => !reduced.matches && !preview && !document.hidden && !document.body.classList.contains('motion-paused');
  const ns='http://www.w3.org/2000/svg';
  let seed=793;
  const random=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
  const el=(tag,attrs={})=>{const node=document.createElementNS(ns,tag);for(const [k,v] of Object.entries(attrs))node.setAttribute(k,v);return node;};
  let pointer={x:-1000,y:-1000};
  if (['spotlight','dots','geometry'].includes(effect)) {
    window.addEventListener('pointermove', e => {
      if (!moving() || e.pointerType==='touch') return;
      pointer={x:e.clientX,y:e.clientY};
      host.style.setProperty('--pointer-x',e.clientX+'px');
      host.style.setProperty('--pointer-y',e.clientY+'px');
      host.style.setProperty('--parallax-x',((e.clientX/innerWidth-.5)*20)+'px');
      host.style.setProperty('--parallax-y',((e.clientY/innerHeight-.5)*20)+'px');
    }, {passive:true});
    document.documentElement.addEventListener('pointerleave',()=>{pointer={x:-1000,y:-1000};});
  }
  if (effect==='particles' && (preview || reduced.matches)) {
    const svg=el('svg',{viewBox:'0 0 1200 800',width:'100%',height:'100%'});svg.style.opacity='.15';
    const pts=Array.from({length:50},()=>({x:random()*1200,y:random()*800}));
    pts.forEach((p,i)=>{
      svg.append(el('circle',{cx:p.x,cy:p.y,r:3,fill:'currentColor'}));
      pts.slice(i+1).filter(q=>Math.hypot(q.x-p.x,q.y-p.y)<200).forEach(q=>svg.append(el('line',{x1:p.x,y1:p.y,x2:q.x,y2:q.y,stroke:'currentColor'})));
    });host.append(svg);
  }
  if (effect==='contours') {
    const svg=el('svg',{viewBox:'0 0 1200 900',preserveAspectRatio:'xMidYMid slice',class:'contour-map'});
    for(let i=0;i<28;i++) {const y=i*35-130;svg.append(el('path',{d:`M-100 ${y} C200 ${y-160} 300 ${y+220} 570 ${y+90} S930 ${y-120} 1330 ${y+260}`,fill:'none',stroke:'currentColor','stroke-width':1}));}
    host.append(svg);
  }
  const counts={paper:14,contours:9,aurora:18,spotlight:5,geometry:9,doodles:10};
  if(counts[effect]) {
    const layer=document.createElement('div');layer.className='ambient-layer';host.append(layer);
    for(let i=0;i<counts[effect];i++) {
      const node=document.createElement('span');node.className='ambient-mark';
      node.style.cssText=`left:${5+random()*90}%;top:${4+random()*92}%;--delay:${-random()*36}s;--duration:${effect==='geometry'?36:effect==='doodles'?24:effect==='paper'?28:22+random()*14}s;--turn:${i%2?1:-1};`;
      const svg=el('svg',{viewBox:'0 0 100 100',fill:'none',stroke:'currentColor','stroke-width':1.4});
      if(effect==='geometry') {
        node.style.color=['#ce3725','#daa92b','#265da6'][i%3];
        svg.append(i%3===0?el('circle',{cx:50,cy:50,r:34,fill:'currentColor',stroke:'none'}):i%3===1?el('rect',{x:22,y:22,width:56,height:56,fill:'currentColor',stroke:'none'}):el('path',{d:'M50 12 L88 80 L12 80 Z',fill:'currentColor',stroke:'none'}));
      } else if(effect==='doodles') {
        const paths=['M50 12 L57 39 L86 40 L64 57 L72 86 L49 68 L26 84 L34 57 L12 40 L41 38 Z','M18 57 C18 9 81 7 83 49 C86 87 33 92 30 55 C28 27 66 24 67 50 C69 69 47 70 47 54','M14 72 Q45 24 82 32 M66 18 L84 31 L70 49','M15 62 Q28 23 40 55 T67 50 T88 38','M22 40 Q50 3 81 40 Q97 72 61 83 Q20 98 15 60 Q12 29 45 18'];
        svg.append(el('path',{d:paths[i%paths.length],pathLength:100,'stroke-linecap':'round','stroke-linejoin':'round'}));
      } else if(effect==='contours') svg.append(el('path',{d:'M20 80 Q8 24 80 16 Q85 75 20 80 M20 80 L64 34'}));
      else if(effect==='spotlight') svg.append(el('circle',{cx:50,cy:50,r:40}));
      else svg.append(el('circle',{cx:50,cy:50,r:effect==='paper'?10:6,fill:'currentColor',stroke:'none'}));
      node.append(svg);layer.append(node);
    }
  }
  if(effect==='grid') {const scan=document.createElement('div');scan.className='grid-scan';host.append(scan);}
  const canvasEffect=['stars','lines','dots','grid'].includes(effect);
  let frame=0,previous=0,phase=0,width=0,height=0,color='',canvas,ctx;
  const stars=Array.from({length:65},()=>({x:random(),y:random(),r:.4+random()*1.3}));
  function draw(dt=0) {
    if(!ctx)return;
    phase+=dt/1000;
    ctx.clearRect(0,0,width,height);ctx.fillStyle=ctx.strokeStyle=color;
    if(effect==='stars') {
      ctx.globalAlpha=.35;
      for(const s of stars) {ctx.beginPath();ctx.arc((s.x*width+phase*7.2)%Math.max(width,1),s.y*height,s.r,0,Math.PI*2);ctx.fill();}
    } else if(effect==='lines') {
      ctx.globalAlpha=.13;ctx.lineWidth=1;
      for(let i=0;i<18;i++) {ctx.beginPath();for(let x=0;x<=width+12;x+=12){const y=height*(i+.5)/18+Math.sin(x/210+phase*.16+i*.24)*28;if(x===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}ctx.stroke();}
    } else if(effect==='dots') {
      for(let x=12;x<width;x+=48)for(let y=12;y<height;y+=48){
        const proximity=moving()?Math.max(0,1-Math.hypot(x-pointer.x,y-pointer.y)/160):0;
        const pulse=(1+Math.sin(phase*Math.PI/4-x/180-y/220))/2;
        ctx.globalAlpha=.08+pulse*.16+proximity*.32;ctx.beginPath();ctx.arc(x,y,1+pulse*.7+proximity*1.6,0,Math.PI*2);ctx.fill();
      }
    } else if(effect==='grid') {
      for(let i=0;i<6;i++) {
        const horizontal=i%2===0;const span=horizontal?width:height;
        const pos=(phase*18+span*(i+.5)/6)%(span+90)-45;
        const lane=Math.round((horizontal?height:width)*(i+1)/7/32)*32;
        for(let j=0;j<8;j++) {ctx.globalAlpha=(1-j/8)*.35;const v=pos-j*4;ctx.fillRect(horizontal?v:lane-1,horizontal?lane-1:v,2,2);}
      }
    }
  }
  function resize(){if(!ctx)return;width=host.clientWidth;height=host.clientHeight;const dpr=Math.min(devicePixelRatio||1,2);canvas.width=width*dpr;canvas.height=height*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);color=getComputedStyle(host).color;draw();}
  function tick(now){const dt=previous?Math.min(now-previous,50):0;previous=now;draw(dt);frame=requestAnimationFrame(tick);}
  function sync(){document.body.classList.toggle('ambient-still',!moving());cancelAnimationFrame(frame);previous=0;if(ctx&&moving())frame=requestAnimationFrame(tick);else draw();}
  if(canvasEffect){canvas=document.createElement('canvas');host.append(canvas);ctx=canvas.getContext('2d');resize();window.addEventListener('resize',resize);}
  sync();document.addEventListener('visibilitychange',sync);document.addEventListener('motionchange',sync);reduced.addEventListener('change',sync);
})();
