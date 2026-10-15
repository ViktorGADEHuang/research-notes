"""Compile only the independent C++ teaching examples; never run rm.cv.fans or RL.

Use an installed C++17 compiler. Generated files stay in the ignored .cache folder.
"""
from pathlib import Path
import argparse
import os
import re
import shutil
import subprocess
import textwrap
import tomllib


ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / 'docs/opensource/rm-cv-fans'


def blocks(markdown, language):
    pattern = rf'^([ \t]*)```{language}(?:[ \t][^\n]*)?\n(.*?)^\1```[ \t]*$'
    return [textwrap.dedent(m.group(2)).strip()
            for m in re.finditer(pattern, markdown, re.M | re.S)]


def fenced_blocks(markdown):
    """Keep order and labels to distinguish programs from contextual API fragments."""
    pattern = r'^([ \t]*)```([\w+-]*)([^\n]*)\n(.*?)^\1```[ \t]*$'
    return [(match.group(2), match.group(3), textwrap.dedent(match.group(4)).strip())
            for match in re.finditer(pattern, markdown, re.M | re.S)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler', default=shutil.which('g++'))
    args = parser.parse_args()
    if not args.compiler:
        parser.error('Provide --compiler with the path to an existing C++17 g++ compiler.')
    compiler = Path(args.compiler).resolve()
    if not compiler.is_file():
        parser.error(f'Compiler does not exist: {compiler}')

    output_dir = ROOT / '.cache/rmcv-example-check'
    output_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env['PATH'] = str(compiler.parent) + os.pathsep + env.get('PATH', '')
    checked = 0

    def check(name, source, expected):
        nonlocal checked
        cpp = output_dir / f'{name}.cpp'
        executable = output_dir / (name + ('.exe' if os.name == 'nt' else ''))
        cpp.write_text(source + '\n', encoding='utf-8')
        command = [str(compiler), '-std=c++17', '-Wall', '-Wextra', '-Wpedantic',
                   '-Werror', '-O0', str(cpp), '-o', str(executable)]
        result = subprocess.run(command, capture_output=True, text=True,
                                encoding='utf-8', errors='replace', env=env, timeout=45)
        if result.returncode:
            raise AssertionError(f'{name}: compilation failed\n{result.stdout}{result.stderr}')
        result = subprocess.run([str(executable)], capture_output=True, text=True,
                                encoding='utf-8', env=env, timeout=5, check=True)
        if result.stdout.strip() != expected.strip():
            raise AssertionError(f'{name}: expected {expected!r}, got {result.stdout!r}')
        checked += 1

    examples = {}
    program_count = fragment_count = 0
    for page in sorted(COURSE.glob('*.md')):
        content = page.read_text(encoding='utf-8')
        fences = fenced_blocks(content)
        page_programs = 0
        for index, (language, title, program) in enumerate(fences):
            if language != 'cpp':
                continue
            if not re.search(r'\bint\s+main\s*\(', program):
                if '片段' not in title:
                    raise AssertionError(f'{page.name}: label contextual C++ as a reading fragment')
                fragment_count += 1
                continue
            if '独立教学示例' not in title:
                raise AssertionError(f'{page.name}: label the complete independent C++ example')
            if index + 1 >= len(fences) or fences[index + 1][0] != 'text':
                raise AssertionError(f'{page.name}: provide output directly after the program')
            expected = fences[index + 1][2]
            page_programs += 1
            examples.setdefault(page.stem, program)
            check(f'{page.stem}-{page_programs}', program, expected)
            program_count += 1
    original_pages = {'cpp-basics', 'cpp-types', 'images', 'math', 'configuration',
                      'estimation', 'reading-lab'}
    assert original_pages <= examples.keys(), 'An original independent example is missing.'

    # Check the exercises using independently calculated outputs and edge cases.
    basic = examples['cpp-basics']
    original = 'brightness{10.0, 20.0, 30.0, 40.0}'
    check('mean-two', basic.replace(original, 'brightness{10.0, 11.0}'), 'mean: 10.5')
    check('mean-empty', basic.replace(original, 'brightness{}'), 'no data')
    check('threshold-strict', examples['images'].replace('>= threshold', '> threshold'),
          'row 1, col 2: 60\nmean: 50.0\n0 0 0\n0 0 255\n255 255 255')
    check('matrix-unit-vector', examples['math'].replace('input{3.0, 4.0}', 'input{1.0, 0.0}'),
          'result: 1 3')
    check('temperature-larger-r', examples['estimation'].replace('noise_variance_c2 = 1.0',
          'noise_variance_c2 = 4.0'),
          'gain: 0.500, estimate: 21.000, variance: 2.000\n'
          'gain: 0.333, estimate: 21.000, variance: 1.333')
    last = examples['reading-lab']
    original = 'values{10.0, 20.0, missing, 300.0, 30.0}'
    # Retain the NaN variable in these inputs so -Werror still checks each example.
    check('brightness-invalid', last.replace(original, 'values{-1.0, missing, 300.0}'),
          'no valid data')
    check('brightness-zero', last.replace(original, 'values{0.0, missing}'),
          'valid mean: 0.0')
    check('brightness-boundaries', last.replace(original, 'values{0.0, 255.0, missing}'),
          'valid mean: 127.5')
    check('brightness-empty', last.replace(original, 'values{}').replace(
          'const double missing =', '[[maybe_unused]] const double missing ='), 'no valid data')

    if 'vision-sampling' in examples:
        sampling = examples['vision-sampling']
        for name, u, v, nearest, linear in [
            ('top-left', '0.0', '0.0', '0.0', '0.0'),
            ('bottom-right', '1.0', '1.0', '200.0', '200.0'),
            ('center', '0.5', '0.5', '200.0', '100.0'),
        ]:
            changed = sampling.replace('u = 0.25;', f'u = {u};').replace('v = 0.5;', f'v = {v};')
            check(f'interpolation-{name}', changed, f'nearest: {nearest}\nbilinear: {linear}')
        constant = sampling.replace('Row{0.0, 100.0}, Row{100.0, 200.0}',
                                    'Row{80.0, 80.0}, Row{80.0, 80.0}')
        check('interpolation-constant', constant, 'nearest: 80.0\nbilinear: 80.0')

    configuration = (COURSE / 'configuration.md').read_text(encoding='utf-8')
    data = tomllib.loads(blocks(configuration, 'toml')[0])
    assert type(data['display']['scale']) is float
    assert type(data['display']['enabled']) is bool
    assert data['display']['title'] == 'Preview'
    print(f'PASS: {program_count} independent C++17 programs, {checked} example/exercise cases; '
          f'documented outputs agree; TOML types checked. {fragment_count} contextual reading '
          'fragments are not standalone builds. Original project and RL were not run.')


if __name__ == '__main__':
    main()
