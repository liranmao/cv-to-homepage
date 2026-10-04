#!/usr/bin/env python3
"""Deploy a generated site to a NEW public GitHub repository. Dry run unless --publish."""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import time
import urllib.request

PROTECTED = {'liranmao/liranmao.github.io', 'liranmao/cv-to-homepage'}


def run(args, cwd=None):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or 'Command failed: ' + args[0])
    return result.stdout.strip()


def check_repo(repo):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9][A-Za-z0-9_.-]*', repo):
        raise ValueError('Use OWNER/REPOSITORY.')
    if repo.lower() in PROTECTED:
        raise ValueError('Protected source/skill repository: ' + repo)
    return repo.split('/')


def deploy(site, repo, publish=False, timeout=240):
    owner, name = check_repo(repo)
    site = Path(site).resolve()
    if not (site / 'docs/.cv-to-homepage').is_file():
        raise ValueError('Choose a site generated with create_site.py.')
    url = 'https://' + owner.lower() + '.github.io/'
    if name.lower() != owner.lower() + '.github.io':
        url += name + '/'
    if not publish:
        print(json.dumps({'repository': repo, 'visibility': 'public', 'source': 'main:/docs',
                          'expected_url': url, 'action': 'Create new repository only. Pass --publish after publication is authorized.'}, indent=2))
        return
    if (site / '.git').exists():
        raise ValueError('Existing Git checkout: refusing automatic deployment. Follow references/deployment.md for recovery or updates.')
    run(['gh', 'auth', 'status'])
    login = run(['gh', 'api', 'user', '--jq', '.login'])
    if login.lower() != owner.lower():
        raise ValueError('Target owner differs from the authenticated account; choose your account or deploy to an organization manually.')
    existing = subprocess.run(['gh', 'api', 'repos/' + repo], capture_output=True, text=True)
    if existing.returncode == 0:
        raise ValueError('Repository already exists; refusing to overwrite it. Choose a new name.')
    if '(HTTP 404)' not in existing.stderr:
        raise RuntimeError('Could not verify repository availability: ' + existing.stderr.strip())
    # Rebuild from the installed engine, never execute scripts from the CV/site directory.
    spec = importlib.util.spec_from_file_location('homepage_build', Path(__file__).resolve().parents[1] / 'assets/site/build.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    data = json.loads((site / 'site.json').read_text(encoding='utf-8'))
    module.validate(data, site)
    data['site_url'] = url
    (site / 'site.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    module.build(site)
    run(['git', 'init', '-b', 'main'], site)
    files = ['docs', 'site.json', 'build.py', 'template.html', 'README.md', '.gitignore', 'LICENSE', 'ATTRIBUTION.md']
    files += [str(p.relative_to(site / 'docs')) for p in (site / 'docs/assets').rglob('*') if p.is_file()]
    run(['git', 'add', '--'] + files, site)
    run(['git', 'commit', '-m', 'Create academic homepage from reviewed CV'], site)
    run(['gh', 'repo', 'create', repo, '--public', '--source', str(site), '--remote', 'origin'], site)
    run(['git', '-c', 'credential.helper=!gh auth git-credential', 'push', '-u', 'origin', 'main'], site)
    run(['gh', 'api', '--method', 'POST', 'repos/' + repo + '/pages', '-f', 'build_type=legacy', '-f', 'source[branch]=main', '-f', 'source[path]=/docs'])
    print('Repository: https://github.com/' + repo, flush=True)
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        metadata = json.loads(run(['gh', 'api', 'repos/' + repo + '/pages']))
        live_url = metadata.get('html_url', url)
        if metadata.get('status') == 'built':
            try:
                with urllib.request.urlopen(live_url, timeout=15) as response:
                    body = response.read().decode('utf-8')
                    if response.status == 200 and module.esc(data['name']) in body:
                        print('Verified live website: ' + live_url)
                        return
            except OSError:
                pass
        if metadata.get('status') == 'errored':
            raise RuntimeError('Pages build failed. Inspect repository Actions before retrying.')
        time.sleep(10)
    print('Deployment requested but live verification is pending: ' + url)
    print('Check gh api repos/' + repo + '/pages and the repository Actions tab. Do not recreate the repository.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--site', type=Path, required=True)
    p.add_argument('--repo', required=True)
    p.add_argument('--publish', action='store_true')
    p.add_argument('--timeout', type=int, default=240)
    a = p.parse_args()
    try:
        deploy(a.site, a.repo, a.publish, a.timeout)
    except (ValueError, RuntimeError, OSError) as e:
        p.exit(1, 'Deployment stopped: ' + str(e) + '\nNo automatic overwrite or force push was attempted.\n')
