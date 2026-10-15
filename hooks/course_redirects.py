"""Keep previously published rm.cv.fans addresses usable after moving the course."""
from html import escape
import json
import os
from pathlib import Path


def on_post_build(config, **kwargs):
    site_dir = Path(config['site_dir']).resolve()
    course_dir = Path(config['docs_dir']) / 'opensource/rm-cv-fans'
    for source in course_dir.glob('*.md'):
        section = Path() if source.stem == 'index' else Path(source.stem)
        destination = site_dir / 'opensource/rm-cv-fans' / section
        legacy = site_dir / 'vision/rm-cv-fans' / section / 'index.html'
        # A redirect may only be written inside this build's output directory.
        legacy.resolve().relative_to(site_dir)
        if not (destination / 'index.html').is_file():
            raise ValueError(f'Missing migrated course page: {destination}')
        target = Path(os.path.relpath(destination, legacy.parent)).as_posix() + '/'
        link = escape(target, quote=True)
        legacy.parent.mkdir(parents=True, exist_ok=True)
        legacy.write_text(
            '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="robots" content="noindex">'
            '<title>教程已移至开源资料教程</title>'
            f'<script>window.location.replace({json.dumps(target)}'
            '+window.location.search+window.location.hash);</script>'
            f'<noscript><meta http-equiv="refresh" content="0;url={link}"></noscript>'
            '</head><body><main><h1>教程已移至开源资料教程</h1>'
            f'<p><a href="{link}">继续阅读 rm.cv.fans 教程</a></p>'
            '</main></body></html>', encoding='utf-8',
        )
