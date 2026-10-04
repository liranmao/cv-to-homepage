#!/usr/bin/env python3
"""Rebuild the public demo with placeholder content and images."""
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
    (media / 'avatar.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240"><rect width="240" height="240" fill="#e9eff5"/><circle cx="120" cy="120" r="96" fill="#d5e0ed"/><text x="120" y="131" text-anchor="middle" font-family="Georgia,serif" font-size="36" fill="#060771">Your photo</text></svg>')
    for i in range(2):
        (media / ('paper-' + str(i) + '.svg')).write_text('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="185" viewBox="0 0 300 185"><rect width="300" height="185" fill="#f0f4f8"/><rect x="20" y="20" width="260" height="145" rx="4" fill="none" stroke="#c0cbd9" stroke-dasharray="5 5"/><text x="150" y="103" text-anchor="middle" font-family="Georgia,serif" font-size="22" fill="#58677c">Publication image</text></svg>')
    data = json.loads((site / 'site.json').read_text())
    data['avatar'] = 'assets/media/avatar.svg'
    data['site_url'] = 'https://liranmao.github.io/cv-to-homepage/'
    data['links'] = [{'label': 'Get this skill', 'url': 'https://github.com/liranmao/cv-to-homepage'}]
    for i, pub in enumerate(data['publications']):
        pub['image'] = 'assets/media/paper-' + str(i) + '.svg'
        pub['badge'] = 'Venue name'
    (site / 'site.json').write_text(json.dumps(data, indent=2))
    create.engine().build(site)
    destination = ROOT / 'docs'
    if destination.exists():
        if not (destination / '.cv-to-homepage').is_file():
            raise SystemExit('Refusing to replace an unmanaged docs directory.')
        shutil.rmtree(destination)
    shutil.copytree(site / 'docs', destination)
print(ROOT / 'docs')
