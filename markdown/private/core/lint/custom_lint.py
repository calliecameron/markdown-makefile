import argparse
import sys
from collections.abc import Sequence

CURLY_QUOTES = "“”‘’"  # noqa: RUF001
CURLY_QUOTE_MSG = "Literal curly quotes must be backslash-escaped."
EN_DASH_MSG = "Literal en-dashes must be replaced with '--'"
EM_DASH_MSG = "Literal em-dashes must be replaced with '---'"
ELLIPSIS_MSG = "Literal ellipses must be replaced with '...'"


def lint(data: Sequence[str]) -> list[tuple[int, int, str]]:
    problems = []

    for row in range(len(data)):
        line = data[row]
        for col in range(len(line)):
            if line[col] in CURLY_QUOTES and (col == 0 or line[col - 1] != "\\"):
                problems.append((row, col, CURLY_QUOTE_MSG))  # noqa: PERF401

        col = line.find("–")  # noqa: RUF001
        if col != -1:
            problems.append((row, col, EN_DASH_MSG))

        col = line.find("—")
        if col != -1:
            problems.append((row, col, EM_DASH_MSG))

        col = line.find("…")
        if col != -1:
            problems.append((row, col, ELLIPSIS_MSG))

    return problems


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file")
    parser.add_argument("out_file")
    args = parser.parse_args()

    with open(args.in_file, encoding="utf-8") as f:
        data = f.read().split("\n")

    problems = lint(data)

    if problems:
        msg = ["ERROR: linting failed"]
        for row, col, problem in problems:
            msg.append(f"row {row + 1} col {col + 1}: {problem}")
        sys.stderr.write("\n\n".join(msg) + "\n\n")
        sys.exit(1)

    with open(args.out_file, mode="w", encoding="utf-8") as f:
        f.write("OK\n")


if __name__ == "__main__":
    main()
