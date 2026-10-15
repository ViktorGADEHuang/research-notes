"""检查教程、站内链接与正文代码，确保网站没有示例下载资源；不执行 RL。"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import ast
import re
import textwrap
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
        self.pre_depth = self.pre_code_depth = 0
        self.pre_blocks, self.block_text = [], []
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
        if tag == 'pre':
            self.pre_depth += 1
        if tag == 'code' and self.pre_depth:
            self.pre_code_depth += 1
            if self.pre_code_depth == 1:
                self.block_text = []

    def handle_endtag(self, tag):
        if tag == 'article':
            self.article = max(0, self.article - 1)
        if tag in ('code', 'pre'):
            self.code = max(0, self.code - 1)
        if tag == 'code' and self.pre_code_depth:
            self.pre_code_depth -= 1
            if not self.pre_code_depth:
                self.pre_blocks.append(''.join(self.block_text).strip())
        if tag == 'pre':
            self.pre_depth = max(0, self.pre_depth - 1)

    def handle_data(self, data):
        if self.pre_code_depth:
            self.block_text.append(data)
        if self.article and not self.code and '```' in data:
            self.raw_fence = True


def check(condition, message):
    if not condition:
        errors.append(message)


def code_blocks(text, language):
    """读取普通、带标题及折叠答案中的围栏；只移除 Markdown 的公共缩进。"""
    pattern = rf'^([ \t]*)```{re.escape(language)}(?:[ \t][^\n]*)?\n(.*?)^\1```[ \t]*$'
    return [textwrap.dedent(match.group(2)).strip()
            for match in re.finditer(pattern, text, re.M | re.S)]


def all_fenced_blocks(text):
    """收集所有普通代码围栏，包括命令、输出及折叠练习，不执行内容。"""
    pattern = r'^([ \t]*)```[\w+-]*(?:[ \t][^\n]*)?\n(.*?)^\1```[ \t]*$'
    return [textwrap.dedent(match.group(2)).strip()
            for match in re.finditer(pattern, text, re.M | re.S)]


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

rendered_code_count = 0
for p in DOCS.rglob('*.md'):
    text = p.read_text(encoding='utf-8')
    check(text.count('```') % 2 == 0, f'{p}: 未闭合代码围栏')
    check('\ufffd' not in text, f'{p}: 存在乱码替换字符')
    relative = p.relative_to(DOCS)
    flat = (SITE / relative.with_suffix('.html')).resolve()
    directory = (SITE / relative.with_suffix('') / 'index.html').resolve()
    # MkDocs 可使用目录式或文件式地址；index.md 对应目录的 index.html。
    page = pages.get(flat) if p.name == 'index.md' else pages.get(directory, pages.get(flat))
    check(page is not None, f'{relative}: 缺少构建后的教程页面')
    if page is not None:
        expected_blocks = Counter(all_fenced_blocks(text))
        actual_blocks = Counter(page.pre_blocks)
        for block, count in expected_blocks.items():
            check(actual_blocks[block] >= count,
                  f'{relative}: 代码/命令/输出块未完整呈现: {block.splitlines()[0][:80] if block else "空块"}')
        rendered_code_count += sum(expected_blocks.values())
    # 仅解析语法，包括需要正文提供输入的阅读片段；不导入，不执行。
    for index, block in enumerate(code_blocks(text, 'python'), start=1):
        try:
            ast.parse(block, filename=f'{p}:代码块{index}')
        except SyntaxError as error:
            errors.append(str(error))
    # URDF/MJCF 完整模型先检查 XML 结构；不加载模拟器或执行节点。
    # 局部修改片段可能包含多个兄弟元素，只有完整模型才作为文档解析。
    for index, block in enumerate(code_blocks(text, 'xml'), start=1):
        if re.search(r'<(?:robot|mujoco)\b', block):
            try:
                ET.fromstring(block)
            except ET.ParseError as error:
                errors.append(f'{relative}: XML 模型块 {index} 无法解析: {error}')

for p in DOCS.rglob('*.svg'):
    diagram = ET.parse(p).getroot()
    check('viewBox' in diagram.attrib, f'{p}: 图示缺少缩放坐标')

python_files = list((ROOT / 'examples/rl').glob('*.py'))
check(len(python_files) == 14, '本地 RL 示例缺失')
for p in python_files:
    ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
    chapter = DOCS / 'rl/code' / (p.stem + '.md')
    if chapter.exists():
        blocks = code_blocks(chapter.read_text(encoding='utf-8'), 'python')
        check(p.read_text(encoding='utf-8').strip() in [b.strip() for b in blocks],
              f'网页完整示例与源码不一致: {p.name}')

examples = ROOT / 'examples/cpp'
check(len(list(examples.glob('*.cpp'))) == 13, '本地 C++ 示例缺失')

# 正文保留模型保存等教学内容，但不发布独立源码文件或压缩包。
for folder in (DOCS, SITE):
    for p in folder.rglob('*'):
        # MkDocs 的压缩站点地图供搜索引擎使用，不是教程下载包。
        if p.is_file() and p.name != 'sitemap.xml.gz':
            check(p.suffix.lower() not in {'.zip', '.7z', '.rar', '.tar', '.gz', '.cpp', '.py'},
                  f'网站仍包含示例下载资源: {p.relative_to(ROOT)}')
for path, page in pages.items():
    for link in page.links:
        parsed = urlsplit(link)
        # GitHub 的 blob 页面用于阅读官方接口源码，不是本站的源码下载入口。
        # 仅区分这种网页；raw 源文件、压缩包和本站 examples 路径仍拒绝。
        source_reference = (parsed.scheme == 'https' and parsed.hostname == 'github.com'
                            and re.match(r'^/[^/]+/[^/]+/blob/', parsed.path)
                            and parsed.path.lower().endswith(('.cpp', '.py')))
        download_link = bool(re.search(r'/examples/|\.(?:zip|7z|rar|tar|gz|cpp|py)$',
                                       parsed.path, re.I))
        check(not download_link or source_reference,
              f'{path.relative_to(ROOT)}: 仍包含示例下载链接 {link}')

cmake = (examples / 'CMakeLists.txt').read_text(encoding='utf-8').strip()
tooling = (DOCS / 'programming/cpp/tooling.md').read_text(encoding='utf-8')
check(cmake in code_blocks(tooling, 'cmake'),
      '网页 CMake 配置与本地源码不一致')

# 独立源码与网页完整示例必须一致；练习片段不参与匹配。
for p in examples.glob('*.cpp'):
    chapter = DOCS / 'programming/cpp' / (p.stem + '.md')
    blocks = code_blocks(chapter.read_text(encoding='utf-8'), 'cpp')
    check(p.read_text(encoding='utf-8').strip() in [b.strip() for b in blocks],
          f'网页完整示例与源码不一致: {p.name}')

if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(list(DOCS.rglob("*.md")))} 篇 Markdown、{len(pages)} 个 HTML 页面、'
      f'{rendered_code_count} 个代码/命令/输出块完整呈现、{len(python_files)} 个 Python 文件静态语法、'
      '正文与本地源码一致；无示例下载资源，未运行 RL。')
