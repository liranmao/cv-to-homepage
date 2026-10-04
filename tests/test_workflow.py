import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/cv-to-homepage'


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


create = load('create', SKILL / 'scripts/create_site.py')
build = create.engine()
deploy = load('deploy', SKILL / 'scripts/deploy.py')
install = load('install', ROOT / 'scripts/install.py')


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links = set(), []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        self.links += [attrs[k] for k in ('href', 'src') if k in attrs]


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def make(self, data):
        profile = self.root / 'reviewed.json'
        profile.write_text(json.dumps(data))
        return create.create(profile, self.root / 'website')

    def test_all_student_examples_build_without_broken_local_links(self):
        for example in (ROOT / 'examples').glob('*.json'):
            with self.subTest(example=example.name):
                site = create.create(example, self.root / example.stem)
                html = (site / 'docs/index.html').read_text()
                parsed = Links()
                parsed.feed(html)
                for target in parsed.links:
                    if target.startswith('#'):
                        self.assertIn(target[1:], parsed.ids)
                    elif not target.startswith(('https:', 'http:', 'mailto:')):
                        self.assertTrue((site / 'docs' / target).is_file(), target)
                self.assertNotIn('Pennmedicine', html)
                self.assertFalse((site / 'CNAME').exists())
                self.assertTrue((site / 'docs/.nojekyll').is_file())

    def test_minimal_profile_omits_missing_sections(self):
        site = self.make({'name': '真实姓名', 'language': 'zh', 'education': [{'title': '本科在读'}]})
        html = (site / 'docs/index.html').read_text()
        self.assertIn('教育背景', html)
        self.assertNotIn('id="publications"', html)
        self.assertNotIn('<img', html)

    def test_text_is_escaped_and_dangerous_urls_fail(self):
        site = self.make({'name': '<script>alert(1)</script>', 'about': ['A & B <img src=x onerror=alert(1)>']})
        html = (site / 'docs/index.html').read_text()
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('<script>alert', html)
        for url in ['javascript:alert(1)', '//evil.example', 'https://good.example\nscript', 'https://user:pass@example.com']:
            with self.assertRaises(ValueError):
                build.validate({'name': 'Test', 'links': [{'label': 'Bad', 'url': url}]})

    def test_private_fields_and_hidden_sections_fail(self):
        for data in [{'name': 'Test', 'phone': '123'}, {'name': 'Test', 'education': [{'title': 'Student'}], 'section_order': ['about']}]:
            with self.assertRaises(ValueError):
                build.validate(data)

    def test_media_paths_cannot_escape(self):
        for path in ['assets/../secret.pdf', 'assets/%2e%2e/secret.pdf', '/tmp/secret.pdf', 'https://example.com/image.png', 'assets/..\\secret.pdf']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                build.validate({'name': 'Test', 'avatar': path})

    def test_rebuild_removes_obsolete_public_media(self):
        site = self.make({'name': 'Test'})
        (site / 'assets/media').mkdir()
        (site / 'assets/media/public.pdf').write_bytes(b'%PDF-1.4 test')
        (site / 'assets/media/private-notes.txt').write_text('Never publish this')
        (site / 'site.json').write_text(json.dumps({'name': 'Test', 'cv': 'assets/media/public.pdf'}))
        build.build(site)
        self.assertTrue((site / 'docs/assets/media/public.pdf').exists())
        self.assertFalse((site / 'docs/assets/media/private-notes.txt').exists())
        (site / 'site.json').write_text('{"name":"Test"}')
        build.build(site)
        self.assertFalse((site / 'docs/assets/media/public.pdf').exists())

    def test_existing_directory_is_never_overwritten(self):
        site = self.make({'name': 'Test'})
        with self.assertRaises(ValueError):
            create.create(self.root / 'reviewed.json', site)
        (site / 'docs/.cv-to-homepage').unlink()
        with self.assertRaises(ValueError):
            build.build(site)
        self.assertTrue((site / 'docs/index.html').exists())

    def test_failed_generation_leaves_no_partial_output(self):
        with self.assertRaises(ValueError):
            self.make({'name': 'Test', 'avatar': 'assets/missing.png'})
        self.assertFalse((self.root / 'website').exists())

    def test_deploy_protects_source_and_skill_repositories(self):
        for repo in ['liranmao/liranmao.github.io', 'LIRANMAO/LIRANMAO.GITHUB.IO', 'liranmao/cv-to-homepage', '../bad', 'name/repo;echo']:
            with self.assertRaises(ValueError):
                deploy.check_repo(repo)

    def test_dry_run_performs_no_subprocess_or_network_actions(self):
        site = self.make({'name': 'Test'})
        with patch.object(deploy.subprocess, 'run', side_effect=AssertionError('No command allowed')), contextlib.redirect_stdout(io.StringIO()) as output:
            deploy.deploy(site, 'tester/my-site')
        self.assertIn('https://tester.github.io/my-site/', output.getvalue())
        self.assertFalse((site / '.git').exists())

    def test_existing_remote_aborts_before_local_or_remote_writes(self):
        site = self.make({'name': 'Test'})
        existing = type('Result', (), {'returncode': 0, 'stdout': '{}', 'stderr': ''})()
        with patch.object(deploy, 'run', side_effect=['ok', 'tester']), patch.object(deploy.subprocess, 'run', return_value=existing), self.assertRaises(ValueError):
            deploy.deploy(site, 'tester/my-site', publish=True)
        self.assertFalse((site / '.git').exists())

    def test_both_installations_are_self_contained(self):
        with contextlib.redirect_stdout(io.StringIO()):
            install.install('both', self.root)
        for parent in ['.agents', '.claude']:
            skill = self.root / parent / 'skills/cv-to-homepage'
            self.assertTrue((skill / 'SKILL.md').exists())
            installed = load('installed_' + parent[1:], skill / 'scripts/create_site.py')
            site = installed.create(ROOT / 'examples/undergraduate.json', self.root / (parent[1:] + '-site'))
            self.assertTrue((site / 'docs/index.html').is_file())
        with self.assertRaises(ValueError):
            install.install('both', self.root)

    def test_every_theme_builds_with_its_default_background(self):
        for theme in build.CATALOG['themes']:
            with self.subTest(theme=theme['id']):
                site = create.create(ROOT / 'examples/phd.json', self.root / theme['id'], theme=theme['id'])
                html = (site / 'docs/index.html').read_text()
                self.assertIn('data-theme="' + theme['id'] + '"', html)
                self.assertIn('data-background="' + theme['background'] + '"', html)
                self.assertNotIn('demo-toolbar', html)
                self.assertEqual(json.loads((site / 'site.json').read_text())['theme'], theme['id'])
                # The exported site must rebuild without the installed skill.
                exported = load('exported_' + theme['id'], site / 'build.py')
                exported.build(site)
                self.assertEqual(html, (site / 'docs/index.html').read_text())

    def test_background_overrides_and_invalid_choices(self):
        for effect in build.BACKGROUNDS:
            with self.subTest(effect=effect):
                site = create.create(ROOT / 'examples/phd.json', self.root / effect, theme='editorial', background=effect)
                html = (site / 'docs/index.html').read_text()
                self.assertIn('data-background="' + effect + '"', html)
                self.assertEqual('src="assets/js/particles.min.js"' in html, effect == 'particles')
        for key in ['theme', 'background']:
            with self.assertRaises(ValueError):
                build.validate({'name': 'Test', key: '../invalid'})

    def test_gallery_pages_and_bundle_have_no_broken_local_links(self):
        def check_tree(root):
            for page in root.rglob('*.html'):
                parsed = Links()
                parsed.feed(page.read_text())
                for href in parsed.links:
                    link = urlsplit(href)
                    if link.scheme or link.netloc:
                        continue
                    target = (page.parent / unquote(link.path)).resolve() if link.path else page
                    if target.is_dir():
                        target = target / 'index.html'
                    self.assertTrue(target.is_file(), str(page) + ': ' + href)
                    if link.fragment and target.suffix == '.html':
                        dest = Links()
                        dest.feed(target.read_text())
                        self.assertIn(link.fragment, dest.ids, str(page) + ': ' + href)
        check_tree(ROOT / 'docs')
        with ZipFile(ROOT / 'docs/downloads/background-library.zip') as bundle:
            bundle.extractall(self.root)
        check_tree(self.root / 'background-library')

    def test_background_bundle_is_reproducible(self):
        demo = load('demo_builder', ROOT / 'scripts/build_demo.py')
        a, b = self.root / 'a.zip', self.root / 'b.zip'
        demo.write_bundle(a)
        demo.write_bundle(b)
        self.assertEqual(a.read_bytes(), b.read_bytes())


if __name__ == '__main__':
    unittest.main()
