#!/usr/bin/env python3
"""Render an academic homepage from reviewed public data; Python 3.9+, no packages."""
import argparse
import html
import json
from pathlib import Path
import re
import shutil
from string import Template
from urllib.parse import urlsplit, unquote

LABELS = {
    'en': {'about': 'About Me', 'publications': 'Publications', 'projects': 'Projects',
           'experience': 'Experience', 'education': 'Education', 'awards': 'Awards',
           'skills': 'Skills', 'service': 'Service & Teaching', 'menu': 'Menu'},
    'zh': {'about': '关于我', 'publications': '论文发表', 'projects': '项目经历',
           'experience': '研究与工作经历', 'education': '教育背景', 'awards': '荣誉奖励',
           'skills': '技能', 'service': '教学与服务', 'menu': '菜单'},
}
STRINGS = {'name', 'position', 'affiliation', 'degree', 'email', 'description',
           'site_url', 'avatar', 'cv', 'language', 'publication_note'}
LISTS = {'about', 'links', 'publications', 'projects', 'experience', 'education',
         'awards', 'skills', 'service', 'section_order'}
ENTRY_KEYS = {'title', 'organization', 'dates', 'details', 'url', 'group'}
PUB_KEYS = {'title', 'authors', 'venue', 'year', 'badge', 'notes', 'image', 'links'}
ORDER = ['about', 'publications', 'projects', 'experience', 'education', 'awards', 'skills', 'service']


def esc(value):
    return html.escape(str(value), quote=True)


def safe_url(value, local=False):
    if not isinstance(value, str) or not value or any(c.isspace() or ord(c) < 32 for c in value):
        raise ValueError('Links must be nonempty URLs without whitespace.')
    parts = urlsplit(value)
    if parts.scheme in ('https', 'http') and parts.netloc and not parts.username and not parts.password:
        return value
    decoded = unquote(value)
    if local and not parts.scheme and not parts.netloc and not parts.query and not parts.fragment:
        if decoded.startswith('assets/') and '\\' not in decoded and not any(p in ('..', '.', '') for p in decoded.split('/')):
            return value
    raise ValueError('Use an http(s) URL or, for media, a file under assets/: ' + value)


def local_media(value):
    safe_url(value, local=True)
    if urlsplit(value).scheme:
        raise ValueError('Media must be a local file under assets/: ' + value)
    return unquote(value)


def validate_links(links):
    if not isinstance(links, list):
        raise ValueError('links must be an array.')
    for link in links:
        if not isinstance(link, dict) or set(link) != {'label', 'url'} or not isinstance(link['label'], str) or not link['label'].strip():
            raise ValueError('Each link needs exactly label and url.')
        safe_url(link['url'])


def validate(data, root=None):
    if not isinstance(data, dict):
        raise ValueError('Profile must be a JSON object.')
    unknown = set(data) - STRINGS - LISTS
    if unknown:
        raise ValueError('Unknown profile fields (possibly private CV data): ' + ', '.join(sorted(unknown)))
    if not isinstance(data.get('name'), str) or not data['name'].strip():
        raise ValueError('name is required.')
    for key in STRINGS & data.keys():
        if not isinstance(data[key], str):
            raise ValueError(key + ' must be text.')
    for key in LISTS & data.keys():
        if not isinstance(data[key], list):
            raise ValueError(key + ' must be an array.')
    if data.get('language', 'en') not in LABELS:
        raise ValueError('language must be en or zh.')
    email = data.get('email', '')
    if email and not re.fullmatch(r'[^\s@<>?&#]+@[^\s@<>?&#]+\.[^\s@<>?&#]+', email):
        raise ValueError('email must be a plain email address.')
    if data.get('site_url'):
        safe_url(data['site_url'])
    validate_links(data.get('links', []))
    order = data.get('section_order', ORDER)
    if any(k not in ORDER for k in order) or len(order) != len(set(order)):
        raise ValueError('section_order must contain unique known section names.')
    missing = [k for k in ORDER if data.get(k) and k not in order]
    if missing:
        raise ValueError('section_order would hide populated sections: ' + ', '.join(missing))
    for key in ['about', 'awards', 'skills']:
        if any(not isinstance(x, str) for x in data.get(key, [])):
            raise ValueError(key + ' must contain only text.')
    for key in ['projects', 'experience', 'education', 'service', 'publications']:
        for item in data.get(key, []):
            keys = PUB_KEYS if key == 'publications' else ENTRY_KEYS
            if not isinstance(item, dict) or set(item) - keys or not isinstance(item.get('title'), str) or not item['title'].strip():
                raise ValueError(key + ': each entry needs a title and only documented fields.')
            for field, value in item.items():
                if field == 'links':
                    validate_links(value)
                elif field == 'details':
                    if not isinstance(value, list) or any(not isinstance(x, str) for x in value):
                        raise ValueError('details must be a list of text.')
                elif not isinstance(value, str):
                    raise ValueError(field + ' must be text.')
            if item.get('url'):
                safe_url(item['url'])
    media = [data.get('avatar'), data.get('cv')] + [p.get('image') for p in data.get('publications', [])]
    for path in filter(None, media):
        relative = local_media(path)
        if root:
            target = (root / relative).resolve()
            assets_root = (root / 'assets').resolve()
            if assets_root not in target.parents or not target.is_file():
                raise ValueError('Missing or unsafe media file: ' + path)
    return data


def link(label, url, css=''):
    return '<a class="{}" href="{}">{}</a>'.format(css, esc(url), esc(label))


def render(data, template):
    labels = LABELS[data.get('language', 'en')]
    profile = ''
    if data.get('avatar'):
        profile += '<span class="image avatar"><img src="{}" alt="{}"></span>'.format(esc(data['avatar']), esc(data['name']))
    profile += '<h1>{}</h1>'.format(esc(data['name']))
    position = ', '.join(filter(None, [data.get('position'), data.get('affiliation')]))
    if position:
        profile += '<p class="position">{}</p>'.format(esc(position))
    if data.get('degree'):
        profile += '<p class="degree">{}</p>'.format(esc(data['degree']))
    if data.get('email'):
        profile += '<p class="email">' + link(data['email'], 'mailto:' + data['email']) + '</p>'
    social = [link(x['label'], x['url']) for x in data.get('links', [])]
    if data.get('cv'):
        social.append(link('CV', data['cv']))
    profile += '<div class="profile-links">' + ' '.join(social) + '</div>'
    sections, nav = [], []
    for key in data.get('section_order', ORDER):
        values = data.get(key, [])
        if not values:
            continue
        anchor = 'about-me' if key == 'about' else key
        nav.append(link(labels[key], '#' + anchor, 'normal'))
        content = ''
        if key == 'about':
            content = ''.join('<p>{}</p>'.format(esc(x)) for x in values)
        elif key in ('awards', 'skills'):
            content = '<ul>' + ''.join('<li>{}</li>'.format(esc(x)) for x in values) + '</ul>'
        elif key == 'publications':
            if data.get('publication_note'):
                content += '<p class="publication-note">{}</p>'.format(esc(data['publication_note']))
            content += '<div class="publications"><ol class="bibliography">'
            for pub in values:
                content += '<li><div class="pub-row">'
                if pub.get('image'):
                    content += '<div class="abbr"><img class="teaser" src="{}" alt="Figure for {}" loading="lazy">'.format(esc(pub['image']), esc(pub['title']))
                    if pub.get('badge'):
                        content += '<span class="badge">{}</span>'.format(esc(pub['badge']))
                    content += '</div>'
                content += '<div class="pub-body"><div class="title">{}</div>'.format(esc(pub['title']))
                content += '<div class="author">{}</div>'.format(esc(pub.get('authors', '')))
                venue = ' · '.join(filter(None, [pub.get('venue'), pub.get('year')]))
                content += '<div class="periodical"><em>{}</em></div>'.format(esc(venue))
                content += '<div class="links">' + ' '.join(link(x['label'], x['url'], 'btn') for x in pub.get('links', [])) + '</div>'
                if pub.get('notes'):
                    content += '<p class="pub-note">{}</p>'.format(esc(pub['notes']))
                content += '</div></div></li>'
            content += '</ol></div>'
        else:
            previous_group = None
            for item in values:
                group = item.get('group')
                if group and group != previous_group:
                    content += '<h3>{}</h3>'.format(esc(group))
                previous_group = group
                title = link(item['title'], item['url']) if item.get('url') else esc(item['title'])
                content += '<div class="entry"><p><strong>{}</strong>'.format(title)
                if item.get('organization'):
                    content += '<br><em>{}</em>'.format(esc(item['organization']))
                if item.get('dates'):
                    content += ' <span class="dates">({})</span>'.format(esc(item['dates']))
                content += '</p>'
                if item.get('details'):
                    content += '<ul>' + ''.join('<li>{}</li>'.format(esc(x)) for x in item['details']) + '</ul>'
                content += '</div>'
        sections.append('<article aria-labelledby="{0}"><h2 id="{0}">{1}</h2>{2}</article>'.format(anchor, labels[key], content))
    canonical = '<link rel="canonical" href="{}">'.format(esc(data['site_url'])) if data.get('site_url') else ''
    return Template(template).substitute(
        lang='zh-CN' if data.get('language') == 'zh' else 'en',
        title=esc(' | '.join(filter(None, [data['name'], data.get('affiliation')]))),
        description=esc(data.get('description') or ' '.join(data.get('about', []))[:180]),
        canonical=canonical, profile=profile, navigation=''.join(nav), sections='\n'.join(sections), menu=labels['menu'])


def build(root):
    root = Path(root).resolve()
    data = validate(json.loads((root / 'site.json').read_text(encoding='utf-8')), root)
    rendered = render(data, (root / 'template.html').read_text(encoding='utf-8'))
    docs = root / 'docs'
    marker = docs / '.cv-to-homepage'
    if docs.is_symlink() or (docs.exists() and not marker.is_file()):
        raise ValueError('Refusing to replace unmanaged docs directory.')
    if docs.exists():
        shutil.rmtree(docs)
    docs.mkdir()
    # Only referenced media plus shipped CSS/JS belong in the public artifact.
    for folder in ['css', 'js']:
        for source in (root / 'assets' / folder).glob('*'):
            if source.is_file() and not source.is_symlink() and source.suffix in ('.css', '.js'):
                dest = docs / 'assets' / folder / source.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest)
    media = [data.get('avatar'), data.get('cv')] + [p.get('image') for p in data.get('publications', [])]
    for relative in filter(None, media):
        relative = local_media(relative)
        dest = docs / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / relative, dest)
    (docs / 'index.html').write_text(rendered, encoding='utf-8')
    (docs / '.nojekyll').touch()
    marker.write_text('Generated public site. Rebuild with python3 build.py.\n')
    for name in ['LICENSE', 'ATTRIBUTION.md']:
        if (root / name).is_file():
            shutil.copy2(root / name, docs / name)
    return docs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    try:
        print(build(args.root))
    except (ValueError, OSError) as error:
        parser.exit(1, 'Build failed: ' + str(error) + '\n')
