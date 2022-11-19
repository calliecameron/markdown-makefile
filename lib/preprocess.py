#!/usr/bin/env python3

from typing import Dict, List, Optional, Tuple
import argparse
import re
import sys

# pylint: disable=consider-using-enumerate

CURLY_QUOTES = '“”‘’'
INCLUDE_MSG = ("Incorrectly-formatted include. Must be '!include //<md_library target>', e.g. "
               "'!include //foo:bar'. Got '%s'.")
CURLY_QUOTE_MSG = 'Literal curly quotes must be backslash-escaped.'
EN_DASH_MSG = "Literal en-dashes must be replaced with '--'"
EM_DASH_MSG = "Literal em-dashes must be replaced with '---'"
ELLIPSIS_MSG = "Literal ellipses must be replaced with '...'"


def process_include(line: str) -> Optional[str]:
    match = re.fullmatch(r'!include //(?P<package>[^:]+)(:(?P<target>.+))?', line)
    if match is None:
        return None
    groups = match.groupdict()
    if 'package' not in groups:
        return None
    package = groups['package']
    if 'target' in groups and groups['target']:
        target = groups['target']
    else:
        target = package.split('/')[-1]
    return package + ':' + target


def preprocess(data: List[str], deps: Dict[str, str]) -> List[Tuple[int, int, str]]:
    problems = []
    used_deps = set()
    declared_deps = frozenset(deps)

    for row in range(len(data)):
        line = data[row]
        if line.startswith('!include'):
            target = process_include(line)
            if not target:
                problems.append((row, 0, INCLUDE_MSG % line))
                continue
            used_deps.add(target)
            if target in deps:
                data[row] = f'!include {deps[target]}'
            continue

        for col in range(len(line)):
            if line[col] in CURLY_QUOTES:
                if col == 0 or line[col - 1] != '\\':
                    problems.append((row, col, CURLY_QUOTE_MSG))

        col = line.find('–')
        if col != -1:
            problems.append((row, col, EN_DASH_MSG))

        col = line.find('—')
        if col != -1:
            problems.append((row, col, EM_DASH_MSG))

        col = line.find('…')
        if col != -1:
            problems.append((row, col, ELLIPSIS_MSG))

    if used_deps != declared_deps:
        used_only = used_deps - declared_deps
        declared_only = declared_deps - used_deps
        msg = ['Used deps do not match declared deps']
        if used_only:
            msg.append('Used but not declared')
            msg += ['  //' + d for d in sorted(used_only)]
        if declared_only:
            msg.append('Declared but not used')
            msg += ['  //' + d for d in sorted(declared_only)]
        problems.append((0, 0, '\n'.join(msg)))

    return problems


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file')
    parser.add_argument('out_file')
    parser.add_argument('--dep', action='append', nargs=2, default=[])
    args = parser.parse_args()

    with open(args.in_file, encoding='utf-8') as f:
        data = f.read().split('\n')

    deps = {}
    for dep, file in args.dep:
        deps[dep] = file

    problems = preprocess(data, deps)

    if problems:
        msg = ['ERROR: markdown preprocessing failed']
        for row, col, problem in problems:
            msg.append(f'row {row + 1} col {col + 1}: {problem}')
        sys.stderr.write('\n\n'.join(msg) + '\n\n')
        sys.exit(1)

    with open(args.out_file, mode='w', encoding='utf-8') as f:
        f.write('\n'.join(data))


if __name__ == '__main__':
    main()
