from typing import Any, Dict, List, Optional
import json
import subprocess
import sys


def _pandoc(
        filter_arg: str, filter_filename: str, stdin: str, extra_args: List[str]) -> Dict[str, Any]:
    sys.stderr.write(f"Running pandoc filter '{filter_filename}' on input {stdin}\n")
    try:
        output = subprocess.run(
            [
                'pandoc',
                '--from=markdown-smart',
                '--to=json',
                f'{filter_arg}={filter_filename}',
            ] + extra_args,
            input=stdin, capture_output=True, check=True, encoding='utf-8')
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Pandoc failed, stdout: '{e.stdout}', stderr: '{e.stderr}'") from e
    j = json.loads(output.stdout)
    sys.stderr.write(f'Pandoc AST: {j}\n')
    sys.stderr.write(f'Pandoc stderr: {output.stderr}\n')
    return j


def pandoc_lua_filter(
        filter_filename: str, stdin: str, extra_args: Optional[List[str]] = None) -> Dict[str, Any]:
    return _pandoc('--lua-filter', filter_filename, stdin, extra_args or [])


def pandoc_filter(
        filter_filename: str, stdin: str, extra_args: Optional[List[str]] = None) -> Dict[str, Any]:
    return _pandoc('--filter', filter_filename, stdin, extra_args or [])
