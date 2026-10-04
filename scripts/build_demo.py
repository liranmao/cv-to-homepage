#!/usr/bin/env python3
"""Rebuild the public demo with fictional content and original schematic SVGs."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('create_demo', ROOT / 'skills/cv-to-homepage/scripts/create_site.py')
create = importlib.util.module_from_spec(spec)
spec.loader.exec_module(create)

with tempfile.TemporaryDirectory() as temp:
    site = create.create(ROOT / 'examples/phd.json', Path(temp) / 'site')
    media = site / 'assets/media'
    media.mkdir(parents=True)
    (media / 'avatar.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240"><rect width="240" height="240" fill="#e9eff5"/><circle cx="120" cy="120" r="96" fill="#d5e0ed"/><text x="120" y="141" text-anchor="middle" font-family="Georgia,serif" font-size="68" fill="#060771">AC</text></svg>''')
    for i in range(2):
        circles = ''.join('<circle cx="{}" cy="{}" r="5" fill="{}"/>'.format(24 + (j * 37 + i * 21) % 250, 45 + (j * 29) % 105, ['#536faa', '#bc8494', '#60a6a6'][j % 3]) for j in range(24))
        (media / ('paper-' + str(i) + '.svg')).write_text('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="185" viewBox="0 0 300 185"><rect width="300" height="185" fill="#f0f4f8"/><path d="M20 35 V160 H280" stroke="#a3b2c7" fill="none"/>' + circles + '<text x="150" y="180" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#58677c">Illustrative diagram · fictional example</text></svg>')
    data = json.loads((site / 'site.json').read_text())
    data['avatar'] = 'assets/media/avatar.svg'
    data['site_url'] = 'https://liranmao.github.io/cv-to-homepage/'
    data['links'] = [{'label': 'Get this skill', 'url': 'https://github.com/liranmao/cv-to-homepage'}]
    for i, pub in enumerate(data['publications']):
        pub['image'] = 'assets/media/paper-' + str(i) + '.svg'
        pub['badge'] = 'Demo only'
    (site / 'site.json').write_text(json.dumps(data, indent=2))
    create.engine().build(site)
    destination = ROOT / 'docs'
    if destination.exists():
        if not (destination / '.cv-to-homepage').is_file():
            raise SystemExit('Refusing to replace an unmanaged docs directory.')
        shutil.rmtree(destination)
    shutil.copytree(site / 'docs', destination)
print(ROOT / 'docs')
