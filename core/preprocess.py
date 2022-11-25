from typing import Dict, List, Optional, Tuple
import argparse
import sys
import bazel_package

# pylint: disable=consider-using-enumerate

INCLUDE = '!include'
CURLY_QUOTES = '“”‘’'
INCLUDE_MSG = ("Incorrectly-formatted include. Must be '!include <md_library label>', e.g. "
               "'!include //foo:bar'. %s, %s")
CURLY_QUOTE_MSG = 'Literal curly quotes must be backslash-escaped.'
EN_DASH_MSG = "Literal en-dashes must be replaced with '--'"
EM_DASH_MSG = "Literal em-dashes must be replaced with '---'"
ELLIPSIS_MSG = "Literal ellipses must be replaced with '...'"


def get_include(line: str, current_package: str) -> Optional[str]:
    if not line.startswith(INCLUDE):
        return None
    label = line[len(INCLUDE):]
    if not label.startswith(' '):
        raise ValueError(f'Include statement must be followed by a space: {line}')
    label = label.lstrip(' ')
    package, target = bazel_package.canonicalise_label(label, current_package)
    return package + ':' + target


def preprocess(
        data: List[str], deps: Dict[str, str], current_package: str) -> List[Tuple[int, int, str]]:
    problems = []
    used_deps = set()
    declared_deps = frozenset(deps)

    for row in range(len(data)):
        line = data[row]
        try:
            target = get_include(line, current_package)
            if target:
                used_deps.add(target)
                if target in deps:
                    data[row] = f'!include {deps[target]}'
                continue
        except ValueError as e:
            problems.append((row, 0, INCLUDE_MSG % (line, e)))
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
    parser.add_argument('current_package')
    parser.add_argument('--dep', action='append', nargs=2, default=[])
    args = parser.parse_args()

    with open(args.in_file, encoding='utf-8') as f:
        data = f.read().split('\n')

    deps = {}
    for dep, file in args.dep:
        deps[dep] = file

    problems = preprocess(data, deps, args.current_package)

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
