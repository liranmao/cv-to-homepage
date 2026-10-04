// Demo-only controls; not included in generated personal websites.
(() => {
 const catalog=JSON.parse(document.getElementById('demo-data').textContent);
 const params=new URLSearchParams(location.search);
 const bg=params.get('background');
 if(bg==='none'||catalog.effects.some(e=>e.id===bg))document.body.dataset.background=bg;
 if(params.has('preview'))document.body.classList.add('preview-static');
 const picker=document.getElementById('demo-background');picker.value=document.body.dataset.background;
 const selection=()=>`../../?theme=${document.body.dataset.theme}&background=${document.body.dataset.background}#selection`;
 document.getElementById('use-style').href=selection();
 picker.addEventListener('change',()=>{const url=new URL(location.href);url.searchParams.set('background',picker.value);location.href=url;});
 document.getElementById('copy-style').addEventListener('click',async e=>{
 const text=`使用 $cv-to-homepage，根据我的简历建立个人网站。风格：${document.body.dataset.theme}；背景：${document.body.dataset.background}。创建新的公开 GitHub 仓库并部署到 GitHub Pages。`;
 try{await navigator.clipboard.writeText(text);e.target.textContent='已复制';}catch{location.href=selection();}
 });
})();
