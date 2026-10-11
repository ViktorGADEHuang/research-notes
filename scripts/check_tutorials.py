"""检查构建后的教程、站内链接与代码包；不导入或执行任何 RL 示例。"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import ast
import re
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOCS, SITE = ROOT / 'docs', ROOT / 'site'
errors = []


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.links = set(), []
        self.article = self.code = 0
        self.raw_fence = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])
        if tag == 'article':
            self.article += 1
        if tag in ('code', 'pre'):
            self.code += 1

    def handle_endtag(self, tag):
        if tag == 'article':
            self.article = max(0, self.article - 1)
        if tag in ('code', 'pre'):
            self.code = max(0, self.code - 1)

    def handle_data(self, data):
        if self.article and not self.code and '```' in data:
            self.raw_fence = True


def check(condition, message):
    if not condition:
        errors.append(message)


pages = {p.resolve(): Page(p.read_text(encoding='utf-8')) for p in SITE.rglob('*.html')}
check(bool(pages), '请先执行 mkdocs build --strict')
for path, page in pages.items():
    check(not page.raw_fence, f'{path.relative_to(ROOT)}: 代码围栏显示为正文')
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = ((SITE / unquote(url.path).lstrip('/')) if url.path.startswith('/')
                  else path.parent / unquote(url.path)) if url.path else path
        if target.is_dir():
            target /= 'index.html'
        target = target.resolve()
        check(target.exists(), f'{path.relative_to(ROOT)}: 缺少目标 {link}')
        if url.fragment and target in pages:
            check(unquote(url.fragment) in pages[target].ids,
                  f'{path.relative_to(ROOT)}: 缺少锚点 {link}')

for p in DOCS.rglob('*.md'):
    text = p.read_text(encoding='utf-8')
    check(text.count('```') % 2 == 0, f'{p}: 未闭合代码围栏')
    check('\ufffd' not in text, f'{p}: 存在乱码替换字符')
    # 仅解析语法，包括需要正文提供输入的阅读片段；不导入，不执行。
    for block in re.findall(r'^```python\s*\n(.*?)^```', text, re.M | re.S):
        ast.parse(block, filename=str(p))

for p in DOCS.rglob('*.svg'):
    diagram = ET.parse(p).getroot()
    check('viewBox' in diagram.attrib, f'{p}: 图示缺少缩放坐标')

python_files = list((DOCS / 'rl/examples').glob('*.py'))
for p in python_files:
    ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
    chapter = DOCS / 'rl/code' / (p.stem + '.md')
    if chapter.exists():
        blocks = re.findall(r'^```python\s*\n(.*?)^```', chapter.read_text(encoding='utf-8'), re.M | re.S)
        check(p.read_text(encoding='utf-8').strip() in [b.strip() for b in blocks],
              f'网页完整示例与源码不一致: {p.name}')

examples = DOCS / 'programming/cpp/examples'
with zipfile.ZipFile(examples / 'cpp-examples.zip') as bundle:
    for p in examples.iterdir():
        if p.suffix not in ('.cpp', '.txt', '.md'):
            continue
        matches = [n for n in bundle.namelist() if Path(n).name == p.name]
        check(len(matches) == 1 and bundle.read(matches[0]) == p.read_bytes(),
              f'下载包与源码不一致: {p.name}')

# 独立源码与网页完整示例必须一致；练习片段不参与匹配。
for p in examples.glob('*.cpp'):
    chapter = DOCS / 'programming/cpp' / (p.stem + '.md')
    blocks = re.findall(r'^```cpp\s*\n(.*?)^```', chapter.read_text(encoding='utf-8'), re.M | re.S)
    check(p.read_text(encoding='utf-8').strip() in [b.strip() for b in blocks],
          f'网页完整示例与源码不一致: {p.name}')

if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(list(DOCS.rglob("*.md")))} 篇 Markdown、{len(pages)} 个 HTML 页面、'
      f'{len(python_files)} 个 Python 文件静态语法、C++ 示例与下载包一致；未运行 RL。')
