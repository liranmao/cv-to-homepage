'use strict';
const catalog = JSON.parse(document.getElementById('gallery-data').textContent);
const themeSelect=document.getElementById('theme-choice');
const backgroundSelect=document.getElementById('background-choice');
const promptBox=document.getElementById('selection-prompt');
const params=new URLSearchParams(location.search);
let tone='全部';
function filterCards(){
 const query=(document.getElementById('search')?.value||'').toLowerCase();let count=0;
 document.querySelectorAll('.design-card').forEach(card=>{
  card.hidden=!((tone==='全部'||card.dataset.tone===tone)&&card.dataset.search.toLowerCase().includes(query));
  if(!card.hidden)count++;
 });
 const empty=document.getElementById('empty-results');if(empty)empty.hidden=count>0;
}
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{
 tone=button.dataset.filter;document.querySelectorAll('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));filterCards();
}));
document.getElementById('search')?.addEventListener('input',filterCards);
function updatePrompt(){
 if(!themeSelect||!backgroundSelect)return;
 const theme=catalog.themes.find(t=>t.id===themeSelect.value);
 const effect=catalog.effects.find(e=>e.id===backgroundSelect.value);
 promptBox.value=`使用 $cv-to-homepage，根据我的简历建立个人网站。\n风格选择「${theme.name}」（theme: ${theme.id}），背景选择「${effect?.name||'纯色'}」（background: ${backgroundSelect.value}）。\n按简历填写内容，创建新的公开 GitHub 仓库并部署到 GitHub Pages。`;
 document.getElementById('selected-preview').href=`styles/${theme.id}/?background=${backgroundSelect.value}`;
 const url=new URL(location.href);url.searchParams.set('theme',theme.id);url.searchParams.set('background',backgroundSelect.value);history.replaceState(null,'',url);
 document.getElementById('copy-status').textContent='';
}
if(themeSelect){
 if(catalog.themes.some(t=>t.id===params.get('theme')))themeSelect.value=params.get('theme');
 const theme=catalog.themes.find(t=>t.id===themeSelect.value);
 backgroundSelect.value=catalog.effects.some(e=>e.id===params.get('background'))||params.get('background')==='none'?params.get('background'):theme.background;
 themeSelect.addEventListener('change',()=>{backgroundSelect.value=catalog.themes.find(t=>t.id===themeSelect.value).background;updatePrompt();});
 backgroundSelect.addEventListener('change',updatePrompt);updatePrompt();
}
document.querySelectorAll('[data-select-theme]').forEach(b=>b.addEventListener('click',()=>{
 themeSelect.value=b.dataset.selectTheme;backgroundSelect.value=catalog.themes.find(t=>t.id===themeSelect.value).background;updatePrompt();document.getElementById('selection').scrollIntoView({behavior:'smooth'});
}));
async function copyText(text,status){
 try {await navigator.clipboard.writeText(text);status.textContent='已复制。粘贴到 Codex 或 Claude Code 即可。';}
 catch {status.textContent='请选中上方指令并复制。';if(promptBox){promptBox.focus();promptBox.select();}}
}
document.getElementById('copy-prompt')?.addEventListener('click',()=>copyText(promptBox.value,document.getElementById('copy-status')));
document.querySelectorAll('[data-copy-effect]').forEach(b=>b.addEventListener('click',()=>copyText(`请在我的网站中使用 cv-to-homepage 素材库的 ${b.dataset.copyEffect} 背景。`,document.getElementById('copy-status'))));
const motion=document.getElementById('motion-toggle');
motion?.addEventListener('click',()=>{
 const paused=document.body.classList.toggle('motion-paused');motion.textContent=paused?'继续动效':'暂停动效';motion.setAttribute('aria-pressed',String(paused));
 document.dispatchEvent(new Event('motionchange'));
 if(window.pJSDom?.[0]) {const p=window.pJSDom[0].pJS;p.particles.move.enable=!paused;if(!paused)p.fn.vendors.draw();}
});

const previewObserver=new ResizeObserver(entries=>{for(const entry of entries){const iframe=entry.target.querySelector('iframe');if(iframe)iframe.style.transform=`scale(${entry.contentRect.width/1200})`;}});
document.querySelectorAll('.preview-shell').forEach(shell=>previewObserver.observe(shell));
