#!/usr/bin/env python3
"""Build the style gallery, complete website previews, and reusable background library."""
import importlib.util
import hashlib
import re
import json
from pathlib import Path
import shutil
import tempfile
from html import escape
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'skills/cv-to-homepage/assets/site'
CATALOG = json.loads((SITE / 'designs.json').read_text(encoding='utf-8'))
DATA = json.dumps(CATALOG, ensure_ascii=False).replace('</', '<\\/')
BASE = 'https://liranmao.github.io/cv-to-homepage/'
spec = importlib.util.spec_from_file_location('create_demo', ROOT / 'skills/cv-to-homepage/scripts/create_site.py')
create = importlib.util.module_from_spec(spec)
spec.loader.exec_module(create)


def nav(prefix='', current='styles'):
    return f'''<header class="site-header"><a class="brand" href="{prefix}index.html">CV / HOMEPAGE<span>个人网站</span></a><nav aria-label="网站导航"><a href="{prefix}index.html" {'aria-current="page"' if current == 'styles' else ''}>网站风格</a><a href="{prefix}library/" {'aria-current="page"' if current == 'library' else ''}>背景素材</a><a href="https://github.com/liranmao/cv-to-homepage#readme">安装 Skill ↗</a></nav></header>'''


def page(title, body, prefix='', attrs='', extra_head=''):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} · CV to Homepage</title><meta name="description" content="浏览个人网站风格，选择背景素材，复制指令交给 AI 建站。"><link rel="stylesheet" href="{prefix}gallery.css">{extra_head}<script src="{prefix}gallery.js" defer></script></head><body class="gallery-page" {attrs}>{body}<script type="application/json" id="gallery-data">{DATA}</script></body></html>'''


def options(items, none=False):
    return ('<option value="none">纯色 · None</option>' if none else '') + ''.join(f'<option value="{x["id"]}">{x["name"]} · {x["english"]}</option>' for x in items)


def overview():
    cards = ''
    for i, t in enumerate(CATALOG['themes'], 1):
        search = escape(' '.join([t['name'], t['english'], t['description'], *t['tags']]), quote=True)
        chips = ''.join(f'<span class="chip">{tag}</span>' for tag in t['tags'])
        cards += f'''<article class="design-card" data-tone="{t['tone']}" data-search="{search}"><div class="preview-shell"><iframe src="styles/{t['id']}/?preview=1" title="{t['name']}缩略预览" loading="lazy" tabindex="-1" aria-hidden="true"></iframe><a class="open-preview" href="styles/{t['id']}/" aria-label="预览{t['name']}"></a></div><div class="card-heading"><h2>{t['name']}</h2><span class="card-number">{i:02}</span></div><p class="english-name">{t['english']}</p><p class="card-description">{t['description']}</p><div class="card-footer"><div class="chips">{chips}</div><button class="text-button" data-select-theme="{t['id']}">选用此风格 ↗</button></div></article>'''
    filters = ''.join(f'<button data-filter="{v}" aria-pressed="{str(v == "全部").lower()}">{v}</button>' for v in ['全部', '浅色', '深色'])
    content = nav() + f'''<main class="gallery-main"><section class="intro intro-title"><h1>个人主页风格模版大全</h1></section><div class="toolbar"><div class="filters" aria-label="按明暗筛选">{filters}</div><input class="search" id="search" type="search" aria-label="搜索风格" placeholder="搜索风格、特点…"></div><section class="design-grid" aria-label="网站风格预览">{cards}</section><p class="empty" id="empty-results" hidden>没有匹配的风格，试试其他关键词。</p><section class="selection" id="selection"><div><div class="eyebrow">Your selection</div><h2>把选择带进你的主页</h2><p>风格决定排版，背景可以另选。复制右侧指令，和简历一起发给 AI。Claude Code 中将 $cv-to-homepage 换成 /cv-to-homepage。</p><div class="selection-controls"><label>网站风格<select id="theme-choice">{options(CATALOG['themes'])}</select></label><label>背景素材<select id="background-choice">{options(CATALOG['effects'], True)}</select></label></div></div><div><textarea class="prompt-box" id="selection-prompt" readonly aria-label="建站指令"></textarea><div class="button-row"><button class="solid-button" id="copy-prompt">复制建站指令</button><a class="outline-button" id="selected-preview" href="styles/classic/">预览这个组合 ↗</a></div><p class="copy-status" id="copy-status" role="status" aria-live="polite"></p></div></section></main><footer class="footnote">CV to Homepage · <a href="library/">浏览背景素材</a> · <a href="https://github.com/liranmao/cv-to-homepage">GitHub ↗</a></footer>'''
    return page('网站风格', content)


def library():
    cards = ''
    for i, e in enumerate(CATALOG['effects'], 1):
        search=escape(' '.join([e['name'],e['english'],e['description']]),quote=True)
        cards += f'''<article class="design-card" data-tone="{e['motion']}" data-search="{search}"><div class="preview-shell"><iframe src="{e['id']}/preview.html?preview=1" title="{e['name']}缩略预览" loading="lazy" tabindex="-1" aria-hidden="true"></iframe><a class="open-preview" href="{e['id']}/" aria-label="预览{e['name']}"></a></div><div class="card-heading"><h2>{e['name']}</h2><span class="card-number">{i:02}</span></div><p class="english-name">{e['english']}</p><p class="card-description">{e['description']}</p><div class="card-footer"><div class="chips"><span class="chip">{e['motion']}</span><span class="chip">{e['technology']}</span></div><a class="text-button" href="{e['id']}/">预览与选用 ↗</a></div></article>'''
    resources = ''.join(f'''<a class="source-card" href="{x['url']}"><div class="eyebrow">{x['kind']}</div><h3>{x['name']} ↗</h3><p>{x['description']}</p></a>''' for x in CATALOG['resources'])
    filters = ''.join(f'<button data-filter="{v}" aria-pressed="{str(v == "全部").lower()}">{v}</button>' for v in ['全部']+[kind for kind in ['静态','动态','交互'] if any(e['motion']==kind for e in CATALOG['effects'])])
    body=nav('../','library')+f'''<main class="gallery-main"><section class="intro"><div><div class="eyebrow">Background library</div><h1>给页面加一点气氛</h1></div><div><div class="counts">{len(CATALOG['effects'])} reusable backgrounds</div><p>粒子、纸感、网格、柔光与流线。每张素材卡都有完整预览、参数说明和可复用源码。</p><div class="button-row"><a class="outline-button" href="../downloads/background-library.zip" download>下载素材包 ↓</a></div></div></section><div class="toolbar"><div class="filters" aria-label="按动效筛选">{filters}</div><input class="search" id="search" type="search" aria-label="搜索背景" placeholder="搜索背景、效果…"></div><section class="design-grid" aria-label="背景素材">{cards}</section><p class="empty" id="empty-results" hidden>没有匹配的素材，试试其他关键词。</p><section class="section-head"><div class="eyebrow">More to explore</div><h2>更多素材来源</h2><p>下面是整理好的开源工具与动态案例。上方 {len(CATALOG['effects'])} 种背景已包含在 Skill 中，可直接选用。</p><div class="source-grid">{resources}</div></section></main><footer class="footnote"><a href="../index.html">← 选择网站风格</a> · <a href="../catalog.json" download>下载素材目录 JSON</a></footer>'''
    return page('背景素材库',body,'../')


def effect_page(effect, preview=False):
    dark=effect['id'] in ['stars','aurora','grid']
    colors=('--paper:#111b29;--page:#111b29;--text:#e2e9f4;--ink:#e2e9f4;--accent:#9dc2e5;--subtle:#a4b4c8;--edge:#3c4c60;--recipe-bg:#162337d9;--green:#5a8067' if dark else '--page:#f4f3ee;--ink:#252823;--accent:#556d48')
    extra='''<link rel="stylesheet" href="../../assets/css/effects.css"><script src="../../assets/js/particles.min.js" defer></script><script src="../../assets/js/main.js" defer></script><script src="../../assets/js/effects.js" defer></script><style>#particles-js{position:fixed;inset:0;z-index:-1;pointer-events:none}</style>'''
    background='<div id="particles-js" aria-hidden="true"></div><div id="site-background" aria-hidden="true"></div>'
    if preview:
        return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{effect['english']}</title><link rel="stylesheet" href="../../gallery.css">{extra}</head><body class="asset-preview" data-background="{effect['id']}" style="{colors}">{background}<div class="sample-type">{effect['english']}<small>BACKGROUND / {effect['id'].upper()}</small></div></body></html>'''
    rows=''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k,v in effect['parameters'].items())
    motion_control='<button class="outline-button" id="motion-toggle" aria-pressed="false">暂停动效</button>' if effect['motion'] != '静态' else ''
    body=background+nav('../../','library')+f'''<main class="effect-stage"><section><a class="eyebrow" href="../">← 背景素材库</a><h1>{effect['english']}</h1><p class="effect-lead">{effect['name']}。{effect['description']}</p><div class="button-row"><a class="solid-button" href="../../?background={effect['id']}#selection">搭配网站风格</a>{motion_control}</div></section><aside class="recipe"><div class="eyebrow">Recipe / {effect['id']}</div><h2>素材配方</h2><dl><div><dt>实现</dt><dd>{effect['technology']}</dd></div><div><dt>许可</dt><dd>{effect['license']}</dd></div>{rows}</dl><div class="button-row"><button class="solid-button" data-copy-effect="{effect['id']}">复制素材指令</button><a class="outline-button" href="../../downloads/background-library.zip" download>下载源码</a></div><p class="copy-status" id="copy-status" role="status" aria-live="polite"></p><p><a href="{effect['source']}">技术参考 ↗</a> · <a href="../../catalog.json">目录与参数</a></p></aside></main>'''
    return page(effect['name'],body,'../../',f'data-background="{effect["id"]}" style="{colors}"',extra).replace('class="gallery-page"','class="gallery-page effect-page"')


def write_bundle(dest):
    files={}
    for rel in ['assets/css/effects.css','assets/js/effects.js','assets/js/main.js','assets/js/particles.min.js','THIRD_PARTY_LICENSES.txt','LICENSE','designs.json']:
        files[rel]=(SITE/rel).read_bytes()
    files['index.html']=b'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Background preview</title><link rel="stylesheet" href="assets/css/effects.css"><script src="assets/js/particles.min.js" defer></script><script src="assets/js/main.js" defer></script><script src="assets/js/effects.js" defer></script><style>body{margin:0;background:#f5f0e7;color:#302b26;--accent:#060771;font:20px/1.6 Georgia,serif}#particles-js{position:fixed;inset:0;z-index:-1}main{max-width:720px;margin:20vh auto;padding:30px}h1{font-size:60px}</style></head><body data-background="particles"><div id="particles-js" aria-hidden="true"></div><div id="site-background" aria-hidden="true"></div><main><h1>Your background</h1><p>Change body[data-background] to choose another effect.</p></main></body></html>'''
    files['README.md']='''# 背景素材包 / Background library

打开 index.html 预览。修改 body 的 data-background 选择效果：
particles, paper, dots, grid, aurora, stars, contours, spotlight, mesh, lines, geometry, doodles, none。

将 assets/ 复制到你的网站，并保留示例中的样式表、脚本和两个背景容器。用 --accent 设置背景主色。深色星野可配 #111b29 底色和 #9dc2e5 强调色。

Open index.html. Set body[data-background] to one of the IDs above. Copy assets/ and the example's stylesheet, scripts, and background containers into your site. Use --accent for the effect color. A dark starfield can use #111b29 for the page and #9dc2e5 for the accent.

素材参数和参考链接见 designs.json。particles.js 使用 MIT 许可，其余素材使用 CC0。许可全文随包提供。
Parameters and references are in designs.json. particles.js is MIT licensed; the other effects are CC0. Full licenses are included.
'''.encode()
    dest.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(dest,'w',ZIP_DEFLATED) as z:
        for name,data in sorted(files.items()):
            info=ZipInfo('background-library/'+name,date_time=(2026,1,1,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,data)


def main():
    with tempfile.TemporaryDirectory() as temp:
        output=Path(temp)/'gallery';output.mkdir()
        for name in ['gallery.css','gallery.js','demo.js']:
            shutil.copy2(ROOT/'gallery'/name,output/name)
        shutil.copytree(SITE/'assets',output/'assets')
        for name in ['LICENSE','ATTRIBUTION.md','THIRD_PARTY_LICENSES.txt']:
            shutil.copy2(SITE/name,output/name)
        (output/'catalog.json').write_text(json.dumps(CATALOG,ensure_ascii=False,indent=2)+'\n')
        for theme in CATALOG['themes']:
            site=create.create(ROOT/'examples/phd.json',Path(temp)/theme['id'],theme=theme['id'])
            media=site/'assets/media';media.mkdir(parents=True)
            (media/'avatar.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240"><rect width="240" height="240" fill="#e9eff5"/><circle cx="120" cy="120" r="96" fill="#d5e0ed"/><text x="120" y="131" text-anchor="middle" font-family="Georgia,serif" font-size="36" fill="#060771">Your photo</text></svg>')
            for i in range(2):
                (media/f'paper-{i}.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="185" viewBox="0 0 300 185"><rect width="300" height="185" fill="#f0f4f8"/><rect x="20" y="20" width="260" height="145" rx="4" fill="none" stroke="#c0cbd9" stroke-dasharray="5 5"/><text x="150" y="103" text-anchor="middle" font-family="Georgia,serif" font-size="22" fill="#58677c">Publication image</text></svg>')
            data=json.loads((site/'site.json').read_text());data['avatar']='assets/media/avatar.svg';data['site_url']=BASE+'styles/'+theme['id']+'/'
            data['links']=[{'label':'Your link','url':'https://example.com'}]
            for i,pub in enumerate(data['publications']):pub['image']=f'assets/media/paper-{i}.svg';pub['badge']='Venue name'
            (site/'site.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
            create.engine().build(site)
            target=output/'styles'/theme['id'];target.parent.mkdir(exist_ok=True);shutil.copytree(site/'docs',target)
            p=target/'index.html';html=p.read_text()
            html=html.replace('<body data-theme=', '<body class="demo-site" data-theme=')
            toolbar=f'''<div class="demo-toolbar"><a href="../../index.html">← 风格总览</a><span class="demo-title">{theme['name']} / {theme['english']}</span><div class="demo-actions"><label>背景 <select id="demo-background">{options(CATALOG['effects'],True)}</select></label><button id="copy-style">复制指令</button><a id="use-style" href="../../#selection">选用 ↗</a></div></div>'''
            html=html.replace('  <a class="skip-link"', toolbar+'\n  <a class="skip-link"')
            html=html.replace('<script src="assets/js/main.js" defer>', '<link rel="stylesheet" href="../../gallery.css"><script src="../../demo.js" defer></script><script src="assets/js/main.js" defer>')
            if 'src="assets/js/particles.min.js"' not in html:html=html.replace('<script src="assets/js/main.js"', '<script src="assets/js/particles.min.js" defer></script><script src="assets/js/main.js"')
            html=html.replace('</body>', f'<script id="demo-data" type="application/json">{DATA}</script></body>')
            p.write_text(html)
        (output/'index.html').write_text(overview())
        (output/'library').mkdir();(output/'library/index.html').write_text(library())
        for effect in CATALOG['effects']:
            folder=output/'library'/effect['id'];folder.mkdir()
            (folder/'index.html').write_text(effect_page(effect))
            (folder/'preview.html').write_text(effect_page(effect,True))
        # A changed asset gets a new URL so returning visitors see the current design.
        for page_path in output.rglob('*.html'):
            def version_asset(match):
                if match.group(2).startswith(('https:', 'http:', '//')):
                    return match.group(0)
                asset=(page_path.parent/match.group(2)).resolve()
                digest=hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
                return match.group(1)+match.group(2)+'?v='+digest+match.group(3)
            page_path.write_text(re.sub(r'((?:href|src)=")([^"?]+\.(?:css|js))(")',version_asset,page_path.read_text()))
        write_bundle(output/'downloads/background-library.zip')
        (output/'.nojekyll').touch();(output/'.cv-to-homepage').write_text('Generated gallery. Rebuild with python3 scripts/build_demo.py.\n')
        destination=ROOT/'docs'
        if destination.exists():
            if not (destination/'.cv-to-homepage').is_file():raise SystemExit('Refusing to replace unmanaged docs directory.')
            shutil.rmtree(destination)
        shutil.copytree(output,destination)
    print(ROOT/'docs')

if __name__=='__main__':main()
