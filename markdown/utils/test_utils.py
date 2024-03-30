import inspect
import json
import os
import subprocess
import sys
import unittest
from collections.abc import Callable, Sequence
from typing import Any, Generic, TypeVar, cast

T = TypeVar("T")
F = TypeVar("F", bound="PandocFilterBase")


class Script:
    def __init__(self, script: str) -> None:
        super().__init__()
        self._script = script

    def run(
        self,
        *,
        args: Sequence[str] | None = None,
        stdin: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [self._script, *(args or [])],
            input=stdin,
            capture_output=True,
            check=True,
            encoding="utf-8",
        )


class PandocFilterBase:
    def __init__(self, pandoc: str, filter_flag: str, filter_filename: str) -> None:
        super().__init__()
        self._script = Script(pandoc)
        self._filter_flag = filter_flag
        self._filter_filename = filter_filename

    def run(
        self,
        *,
        args: Sequence[str] | None = None,
        stdin: str | None = None,
    ) -> dict[str, Any]:
        sys.stderr.write(f"Running pandoc filter '{self._filter_filename}' on input {stdin}\n")
        try:
            output = self._script.run(
                args=[
                    "--from=markdown-smart-auto_identifiers",
                    "--to=json",
                    f"{self._filter_flag}={self._filter_filename}",
                    *(args or []),
                ],
                stdin=stdin,
            )
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Pandoc failed, stdout: '{e.stdout}', stderr: '{e.stderr}'") from e
        j = json.loads(output.stdout)
        sys.stderr.write(f"Pandoc AST: {j}\n")
        sys.stderr.write(f"Pandoc stderr: {output.stderr}\n")
        return cast(dict[str, Any], j)


class PandocFilter(PandocFilterBase):
    def __init__(self, pandoc: str, filter_filename: str) -> None:
        super().__init__(pandoc, "--filter", filter_filename)


class PandocLuaFilter(PandocFilterBase):
    def __init__(self, pandoc: str, filter_filename: str) -> None:
        super().__init__(pandoc, "--lua-filter", filter_filename)


class TestCase(unittest.TestCase):
    @staticmethod
    def tmpdir() -> str:
        tmp = os.getenv("TEST_TMPDIR")
        if not tmp:
            raise ValueError("Couldn't get TEST_TMPDIR")
        return tmp


class RunnerTestCase(TestCase, Generic[T]):
    _runner_constructor: Callable[..., T]
    _runner_instance: T | None = None

    @classmethod
    def _runner_args_needed(cls) -> int:
        return len(inspect.signature(cls._runner_constructor).parameters)

    @classmethod
    def setUpClass(cls) -> None:
        if cls._runner_instance:
            return

        cls._runner_instance = cls._runner_constructor(*sys.argv[1 : cls._runner_args_needed() + 1])

    @classmethod
    def _runner(cls) -> T:
        if not cls._runner_instance:
            raise ValueError("Runner missing")
        return cast(T, cls._runner_instance)

    @classmethod
    def main(cls) -> None:
        if len(sys.argv) < cls._runner_args_needed() + 1:
            raise ValueError("Not enough args")

        unittest.main(argv=[sys.argv[0]] + sys.argv[cls._runner_args_needed() + 1 :])


class ScriptTestCase(RunnerTestCase[Script]):
    _runner_constructor = Script

    def run_script(
        self,
        *,
        args: Sequence[str] | None = None,
        stdin: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return self._runner().run(args=args, stdin=stdin)


class PandocFilterBaseTestCase(RunnerTestCase[F]):
    def run_filter(
        self,
        stdin: str,
        args: Sequence[str] | None = None,
    ) -> dict[str, Any]:
        return self._runner().run(args=args, stdin=stdin)


class PandocFilterTestCase(PandocFilterBaseTestCase[PandocFilter]):
    _runner_constructor = PandocFilter


class PandocLuaFilterTestCase(PandocFilterBaseTestCase[PandocLuaFilter]):
    _runner_constructor = PandocLuaFilter
