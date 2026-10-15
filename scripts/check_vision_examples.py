"""Check only the CV course's marked, standard-library teaching programs.

Never imports RL, the upstream project, NumPy, OpenCV or a learning framework.
Temporary programs stay in the ignored .cache directory.
"""
import ast
from pathlib import Path
import re
import subprocess
import sys
import textwrap


ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / 'docs/vision'
CHAPTERS = ('images', 'arrays', 'color', 'transforms', 'filtering', 'regions',
            'features', 'camera', 'networks', 'detection', 'tracking',
            'evaluation', 'project', 'herding')
ALLOWED_IMPORTS = {'math', 'statistics', 'collections', 'itertools'}


def fenced_blocks(markdown):
    pattern = r'^([ \t]*)```([\w+-]*)([^\n]*)\n(.*?)^\1```[ \t]*$'
    return [(match.group(2), match.group(3), textwrap.dedent(match.group(4)).strip())
            for match in re.finditer(pattern, markdown, re.M | re.S)]


def main():
    output_dir = ROOT / '.cache/vision-example-check'
    output_dir.mkdir(parents=True, exist_ok=True)
    examples = {}

    def run(name, program, expected):
        source = output_dir / f'{name}.py'
        source.write_text(program + '\n', encoding='utf-8')
        result = subprocess.run(
            [sys.executable, '-I', '-X', 'utf8', str(source)],
            capture_output=True, text=True, encoding='utf-8', timeout=5,
        )
        if result.returncode:
            raise AssertionError(f'{name}: {result.stdout}{result.stderr}')
        if result.stdout.strip() != expected.strip():
            raise AssertionError(f'{name}: expected {expected!r}, got {result.stdout!r}')

    for chapter in CHAPTERS:
        page = COURSE / f'{chapter}.md'
        fences = fenced_blocks(page.read_text(encoding='utf-8'))
        marked = [(index, program) for index, (language, title, program) in enumerate(fences)
                  if language == 'python' and '独立教学示例' in title]
        if len(marked) != 1:
            raise AssertionError(f'{page.name}: expected one clearly marked teaching program')
        index, program = marked[0]
        tree = ast.parse(program, filename=str(page))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module] if not node.level else ['relative import']
            else:
                continue
            if any(name not in ALLOWED_IMPORTS for name in names):
                raise AssertionError(f'{page.name}: unexpected dependency: {names}')
        if index + 1 >= len(fences) or fences[index + 1][0] != 'text':
            raise AssertionError(f'{page.name}: expected output must follow the program')
        expected = fences[index + 1][2]
        run(chapter, program, expected)
        examples[chapter] = program

    # Exercise the final integration example's contracts with independent cases:
    # stale/future data, no objects, invalid geometry, exact image boundaries.
    project = examples['project'].rsplit('summarize(frame, now_s=10.1)', 1)[0]
    cases = '''
import copy
import contextlib
import io

assert frame_problem(frame, 10.3) == 'frame too old'
assert frame_problem(frame, 9.9) == 'future timestamp'
assert frame_problem(frame, float('nan')) == 'invalid time'
bad_size = dict(frame, width=0)
assert frame_problem(bad_size, 10.1) == 'invalid image size'
assert box_problem({'label': 'sheep', 'box': (0, 0, 100, 80)}, 100, 80) is None
assert box_problem({'label': 'sheep', 'box': (1, 1, 1, 3)}, 100, 80) == 'non-positive size'
assert box_problem({'label': 'sheep', 'box': (0, 0, float('nan'), 3)}, 100, 80) == 'invalid number'
assert box_problem({'label': 'grass', 'box': (0, 0, 3, 3)}, 100, 80) == 'other category'

def output(record, now):
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        summarize(record, now)
    return stream.getvalue().strip()

assert output(frame, 10.3) == 'frame rejected: frame too old'
empty = dict(frame, records=[])
assert output(empty, 10.1) == ('frame age: 0.100 s\\nvalid boxes: 0\\n'
                               'left/right: 0/0\\nno valid centers')
middle = copy.deepcopy(frame)
middle['records'] = [{'number': 9, 'label': 'sheep', 'box': (40, 10, 60, 30)}]
assert output(middle, 10.1) == ('frame age: 0.100 s\\n'
    'record 9: center=(50.0, 20.0) px, zone=right\\nvalid boxes: 1\\n'
    'left/right: 0/1\\nmean center: (50.0, 20.0) px')
print('PASS: project boundary and missing-data contracts')
'''
    run('project-contracts', project + cases,
        'PASS: project boundary and missing-data contracts')
    print(f'PASS: {len(examples)} CV teaching programs match their printed output; '
          '11 integration contracts; standard library only, no RL or upstream execution.')


if __name__ == '__main__':
    main()
