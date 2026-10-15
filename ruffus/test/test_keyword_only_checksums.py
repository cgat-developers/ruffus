"""Regression coverage for keyword-only defaults in job history."""

from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest

from ruffus import Pipeline
from ruffus.ruffus_utility import (
    CHECKSUM_FUNCTIONS, CHECKSUM_FUNCTIONS_AND_PARAMS,
    CHECKSUM_HISTORY_TIMESTAMPS, JobHistoryChecksum,
)


def function_checksum(func):
    task = SimpleNamespace(user_defined_work_func=func)
    return JobHistoryChecksum("output", 0, [], task).chksum_func


class TestKeywordOnlyChecksums(unittest.TestCase):
    def test_changed_default_changes_checksum(self):
        def task(*, option=1):
            return option

        before = function_checksum(task)
        task.__kwdefaults__["option"] = 2
        self.assertNotEqual(before, function_checksum(task))

    def test_default_dictionary_order_does_not_change_checksum(self):
        def task(*, first=1, second=2):
            return first + second

        before = function_checksum(task)
        task.__kwdefaults__ = {"second": 2, "first": 1}
        self.assertEqual(before, function_checksum(task))

    def test_empty_defaults_are_equivalent_to_no_defaults(self):
        def task():
            pass

        before = function_checksum(task)
        task.__kwdefaults__ = {}
        self.assertEqual(before, function_checksum(task))

    def test_changed_default_reruns_pipeline(self):
        for level in (CHECKSUM_FUNCTIONS, CHECKSUM_FUNCTIONS_AND_PARAMS):
            with self.subTest(checksum_level=level), TemporaryDirectory() as directory:
                output = Path(directory) / "output.txt"
                calls = []

                def task(outfile, *, value="first"):
                    calls.append(value)
                    Path(outfile).write_text(value)

                pipeline = Pipeline(self.id() + str(level))
                pipeline.originate(task, str(output))
                options = dict(
                    verbose=0, multiprocess=1, checksum_level=level,
                    history_file=str(Path(directory) / "history.sqlite"),
                )
                pipeline.run(**options)
                pipeline.run(**options)
                self.assertEqual(calls, ["first"])

                task.__kwdefaults__["value"] = "second"
                # Timestamp-only checks deliberately ignore function changes.
                pipeline.run(**dict(options, checksum_level=CHECKSUM_HISTORY_TIMESTAMPS))
                self.assertEqual(calls, ["first"])
                pipeline.run(**options)
                self.assertEqual(output.read_text(), "second")
                self.assertEqual(calls, ["first", "second"])
                pipeline.run(**options)
                self.assertEqual(calls, ["first", "second"])


if __name__ == "__main__":
    unittest.main()
