const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../skills/cv-to-homepage/assets/site/assets/js/effects.js'),'utf8');
// Test scheduler and accessibility behavior without installing a browser dependency.
function setup(effect,{reduced=false,preview=false}={}){
 const callbacks=new Map(),events=new Map(),mediaEvents=new Map(),windowEvents=new Map();
 let next=1,drawCalls=0;
 const context={setTransform(){},clearRect(){drawCalls++},beginPath(){},arc(){},fill(){},stroke(){},moveTo(){},lineTo(){},fillRect(){}};
 function node(tag){const classes=new Set();return {tag,children:[],attrs:{},style:{setProperty(k,v){this[k]=v}},classList:{add:x=>classes.add(x),contains:x=>classes.has(x),toggle(x,on){const yes=on===undefined?!classes.has(x):on;yes?classes.add(x):classes.delete(x);return yes}},clientWidth:1200,clientHeight:800,setAttribute(k,v){this.attrs[k]=v},append(...kids){this.children.push(...kids)},getContext(){return context},addEventListener(){}};}
 const host=node('div'),body=node('body');body.dataset={background:effect};
 const document={body,hidden:false,documentElement:node('html'),getElementById:()=>host,createElement:node,createElementNS:(ns,tag)=>node(tag),addEventListener:(name,cb)=>events.set(name,cb)};
 const media={matches:reduced,addEventListener:(name,cb)=>mediaEvents.set(name,cb)};
 vm.runInNewContext(source,{document,matchMedia:()=>media,location:{search:preview?'?preview=1':''},URLSearchParams,window:{addEventListener:(name,cb)=>windowEvents.set(name,cb)},innerWidth:1200,innerHeight:800,devicePixelRatio:1,getComputedStyle:()=>({color:'#345'}),requestAnimationFrame:cb=>{const id=next++;callbacks.set(id,cb);return id},cancelAnimationFrame:id=>callbacks.delete(id)});
 return {host,body,document,media,callbacks,events,mediaEvents,windowEvents,draws:()=>drawCalls,frame(now){const pending=[...callbacks.values()];callbacks.clear();pending.forEach(cb=>cb(now));}};
}
for(const effect of ['dots','grid','stars','lines']){
 test(`${effect}: one animation loop, paused and hidden pages stop drawing`,()=>{
  const s=setup(effect);assert.equal(s.callbacks.size,1);s.frame(100);s.frame(116);assert.equal(s.callbacks.size,1);assert.ok(s.draws()>=3);
  s.body.classList.toggle('motion-paused',true);s.events.get('motionchange')();assert.equal(s.callbacks.size,0);assert.ok(s.body.classList.contains('ambient-still'));
  s.body.classList.toggle('motion-paused',false);s.events.get('motionchange')();s.events.get('motionchange')();assert.equal(s.callbacks.size,1);
  s.document.hidden=true;s.events.get('visibilitychange')();assert.equal(s.callbacks.size,0);
  s.document.hidden=false;s.events.get('visibilitychange')();assert.equal(s.callbacks.size,1);
  s.media.matches=true;s.mediaEvents.get('change')();assert.equal(s.callbacks.size,0);
 });
 test(`${effect}: reduced motion and thumbnails render without a loop`,()=>{
  for(const settings of [{reduced:true},{preview:true}]){const s=setup(effect,settings);assert.equal(s.callbacks.size,0);assert.ok(s.draws()>0);assert.ok(s.body.classList.contains('ambient-still'));}
 });
}
test('decorative effects remain visible and respect pause/reduced motion',()=>{
 for(const effect of ['paper','contours','aurora','spotlight','geometry','doodles']){
  const s=setup(effect,{reduced:true});assert.ok(s.host.children.length>0);assert.equal(s.callbacks.size,0);assert.ok(s.body.classList.contains('ambient-still'));
  s.media.matches=false;s.mediaEvents.get('change')();assert.equal(s.body.classList.contains('ambient-still'),false);
  s.body.classList.toggle('motion-paused',true);s.events.get('motionchange')();assert.ok(s.body.classList.contains('ambient-still'));
 }
});
test('pointer parallax ignores touch and reduced-motion input',()=>{
 const s=setup('geometry');const move=s.windowEvents.get('pointermove');move({clientX:1200,clientY:800,pointerType:'mouse'});assert.equal(s.host.style['--parallax-x'],'10px');
 move({clientX:0,clientY:0,pointerType:'touch'});assert.equal(s.host.style['--parallax-x'],'10px');
 s.media.matches=true;s.mediaEvents.get('change')();move({clientX:0,clientY:0,pointerType:'mouse'});assert.equal(s.host.style['--parallax-x'],'10px');
});
