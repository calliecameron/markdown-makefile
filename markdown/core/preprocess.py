import argparse
import re
import sys
from collections.abc import Mapping, MutableSequence, Set

import markdown.utils.bazel_package

INCLUDE = "!include"
INCLUDE_MSG = (
    "Incorrectly-formatted include. Must be '!include <md_file label>' where label "
    "is in deps, e.g. '!include //foo:bar'. %s"
)
IMAGE_MSG = (
    "Incorrectly-formatted image. Must be '![<text>](<label>)' where label is in "
    "'images', e.g. '![foo](//foo:bar)'. %s"
)


def process_include(
    line: str,
    deps: Mapping[str, str],
    current_package: str,
) -> tuple[str, str | None, str | None]:
    if not line.startswith(INCLUDE):
        return line, None, None
    raw_label = line[len(INCLUDE) :]
    if not raw_label.startswith(" "):
        return line, None, f"Include statement must be followed by a space: {line}"
    raw_label = raw_label.lstrip(" ")
    try:
        package, target = markdown.utils.bazel_package.canonicalise_label(
            raw_label,
            current_package,
        )
        label = package + ":" + target
        if label in deps:
            return "!include " + deps[label], label, None
        return line, label, INCLUDE_MSG % label
    except ValueError as e:
        return line, None, INCLUDE_MSG % e


def process_images(
    line: str,
    images: Mapping[str, str],
    current_package: str,
) -> tuple[str, frozenset[str], list[tuple[int, str]]]:
    original_line = line
    problems = []
    labels = set()
    replacements = {}
    for match in re.finditer(r"!\[[^\]]*\]\(([^\)]+)\)", line):
        raw_label = match.group(1)
        try:
            package, target = markdown.utils.bazel_package.canonicalise_label(
                raw_label,
                current_package,
            )
            label = package + ":" + target
            labels.add(label)
            if label in images:
                replacements[raw_label] = images[label]
            else:
                problems.append((match.start(), IMAGE_MSG % label))
        except ValueError as e:
            problems.append((match.start(), IMAGE_MSG % e))
    if problems:
        return original_line, frozenset(labels), problems
    for raw_label, replacement in sorted(replacements.items()):
        line = re.sub(rf"!\[([^\]]*)\]\({re.escape(raw_label)}\)", rf"![\1]({replacement})", line)
    return line, frozenset(labels), []


def check_strict_deps(used: Set[str], declared: Set[str], name: str) -> str | None:
    if used != declared:
        used_only = used - declared
        declared_only = declared - used
        msg = [f"Used {name} do not match declared {name}"]
        if used_only:
            msg.append("Used but not declared")
            msg += ["  //" + d for d in sorted(used_only)]
        if declared_only:
            msg.append("Declared but not used")
            msg += ["  //" + d for d in sorted(declared_only)]
        return "\n".join(msg)
    return None


def preprocess(
    data: MutableSequence[str],
    deps: Mapping[str, str],
    images: Mapping[str, str],
    current_package: str,
) -> list[tuple[int, int, str]]:
    problems = []
    used_deps = set()
    declared_deps = frozenset(deps)
    used_images: Set[str] = set()
    declared_images = frozenset(images)

    for row in range(len(data)):
        line = data[row]
        try:
            new_line, line_dep_used, line_problem = process_include(line, deps, current_package)
            if line_dep_used:
                used_deps.add(line_dep_used)
            if line_problem:
                problems.append((row, 0, line_problem))
            if new_line != line:
                # Since an include takes up a whole line, we don't need to check anything else if
                # we found one.
                line = new_line
                continue

            line, line_images_used, line_problems = process_images(line, images, current_package)
            used_images |= line_images_used
            problems += [(row, col, problem) for col, problem in line_problems]

        finally:
            data[row] = line

    problem = check_strict_deps(frozenset(used_deps), declared_deps, "deps")
    if problem:
        problems.append((0, 0, problem))

    problem = check_strict_deps(frozenset(used_images), declared_images, "images")
    if problem:
        problems.append((0, 0, problem))

    return problems


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file")
    parser.add_argument("out_file")
    parser.add_argument("current_package")
    parser.add_argument("--dep", action="append", nargs=2, default=[])
    parser.add_argument("--image", action="append", nargs=2, default=[])
    args = parser.parse_args()

    with open(args.in_file, encoding="utf-8") as f:
        data = f.read().split("\n")

    deps = {}
    for dep, file in args.dep:
        deps[dep] = file

    images = {}
    for image, file in args.image:
        images[image] = file

    problems = preprocess(data, deps, images, args.current_package)

    if problems:
        msg = ["ERROR: markdown preprocessing failed"]
        for row, col, problem in problems:
            msg.append(f"row {row + 1} col {col + 1}: {problem}")
        sys.stderr.write("\n\n".join(msg) + "\n\n")
        sys.exit(1)

    with open(args.out_file, mode="w", encoding="utf-8") as f:
        f.write("\n".join(data))


if __name__ == "__main__":
    main()
