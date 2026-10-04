#!/usr/bin/env python3
"""Create a fresh website from reviewed public JSON. Does not read a raw CV or publish."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

TEMPLATE = Path(__file__).resolve().parents[1] / 'assets' / 'site'


def engine():
    spec = importlib.util.spec_from_file_location('homepage_build', TEMPLATE / 'build.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def create(profile, output, avatar=None, public_cv=None):
    output = Path(output).expanduser().absolute()
    if output.exists() or output.is_symlink():
        raise ValueError('Output already exists. Choose a new directory; use build.py to update an existing site.')
    data = json.loads(Path(profile).read_text(encoding='utf-8'))
    module = engine()
    module.validate(data)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.homepage-', dir=output.parent) as staging:
        work = Path(staging) / 'site'
        shutil.copytree(TEMPLATE, work, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        for key, source, allowed in [('avatar', avatar, {'.jpg', '.jpeg', '.png', '.webp'}), ('cv', public_cv, {'.pdf'})]:
            if source:
                source = Path(source).expanduser().resolve()
                if source.suffix.lower() not in allowed or not source.is_file():
                    raise ValueError(key + ': unsupported or missing file.')
                relative = 'assets/media/' + key + source.suffix.lower()
                target = work / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
                data[key] = relative
        (work / 'site.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (work / '.gitignore').write_text('.DS_Store\n__pycache__/\n*.pyc\n.private/\n.env*\n')
        (work / 'README.md').write_text('# ' + data['name'] + '\n\n'
            '中文 | [English](README.en.md)\n\n'
            '编辑 `site.json`，运行 `python3 build.py` 生成网站。\n\n'
            '本地预览：`python3 -m http.server 8000 --bind 127.0.0.1 --directory docs`。\n\n'
            'GitHub Pages 发布 `main` 分支的 `/docs`。更新后，提交并推送改动和重建的 `docs/`。\n', encoding='utf-8')
        (work / 'README.en.md').write_text('# ' + data['name'] + '\n\n'
            '[中文](README.md) | English\n\n'
            'Edit `site.json`, then run `python3 build.py` to build the website.\n\n'
            'Local preview: `python3 -m http.server 8000 --bind 127.0.0.1 --directory docs`.\n\n'
            'GitHub Pages publishes `/docs` on the `main` branch. After updating, commit and push your changes and the rebuilt `docs/`.\n', encoding='utf-8')
        module.build(work)
        work.rename(output)
    return output


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--profile', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--avatar', type=Path)
    p.add_argument('--public-cv', type=Path, help='Explicitly publish this reviewed PDF as a downloadable CV.')
    a = p.parse_args()
    try:
        print(create(a.profile, a.output, a.avatar, a.public_cv))
    except (ValueError, OSError) as e:
        p.exit(1, 'Cannot create site: ' + str(e) + '\n')
