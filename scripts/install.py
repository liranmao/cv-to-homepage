#!/usr/bin/env python3
"""Install the self-contained skill into Codex, Claude Code, or both."""
import argparse
from pathlib import Path
import shutil
import tempfile

SOURCE = Path(__file__).resolve().parents[1] / 'skills/cv-to-homepage'


def install(agent, home, update=False):
    agents = ['codex', 'claude'] if agent == 'both' else [agent]
    destinations = [Path(home) / ('.agents/skills' if a == 'codex' else '.claude/skills') / 'cv-to-homepage' for a in agents]
    for dest in destinations:
        if dest.is_symlink():
            raise ValueError('Refusing to replace symlink: ' + str(dest))
        if dest.exists() and not update:
            raise ValueError('Already installed: ' + str(dest) + '. Use --update to replace this skill only.')
    for dest in destinations:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.skill-install-', dir=dest.parent) as temp:
            staged = Path(temp) / 'cv-to-homepage'
            shutil.copytree(SOURCE, staged, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            if dest.exists():
                dest.rename(Path(temp) / 'previous')
            staged.rename(dest)
        print('Installed: ' + str(dest))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--agent', choices=['codex', 'claude', 'both'], required=True)
    p.add_argument('--home', type=Path, default=Path.home(), help='Override home for isolated installation tests.')
    p.add_argument('--update', action='store_true')
    a = p.parse_args()
    try:
        install(a.agent, a.home, a.update)
    except (ValueError, OSError) as e:
        p.exit(1, str(e) + '\n')
