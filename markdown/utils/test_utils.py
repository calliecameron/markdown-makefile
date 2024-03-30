import json
import os
import subprocess
import sys
from collections.abc import Sequence
from typing import Any, cast


def _pandoc(
    pandoc: str,
    filter_arg: str,
    filter_filename: str,
    stdin: str,
    extra_args: Sequence[str],
) -> dict[str, Any]:
    sys.stderr.write(f"Running pandoc filter '{filter_filename}' on input {stdin}\n")
    try:
        output = subprocess.run(
            [
                pandoc,
                "--from=markdown-smart-auto_identifiers",
                "--to=json",
                f"{filter_arg}={filter_filename}",
                *extra_args,
            ],
            input=stdin,
            capture_output=True,
            check=True,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Pandoc failed, stdout: '{e.stdout}', stderr: '{e.stderr}'") from e
    j = json.loads(output.stdout)
    sys.stderr.write(f"Pandoc AST: {j}\n")
    sys.stderr.write(f"Pandoc stderr: {output.stderr}\n")
    return cast(dict[str, Any], j)


def pandoc_lua_filter(
    pandoc: str,
    filter_filename: str,
    stdin: str,
    extra_args: Sequence[str] | None = None,
) -> dict[str, Any]:
    return _pandoc(pandoc, "--lua-filter", filter_filename, stdin, extra_args or [])


def pandoc_filter(
    pandoc: str,
    filter_filename: str,
    stdin: str,
    extra_args: Sequence[str] | None = None,
) -> dict[str, Any]:
    return _pandoc(pandoc, "--filter", filter_filename, stdin, extra_args or [])


def tmpdir() -> str:
    tmp = os.getenv("TEST_TMPDIR")
    if not tmp:
        raise ValueError("Couldn't get TEST_TMPDIR")
    return tmp
