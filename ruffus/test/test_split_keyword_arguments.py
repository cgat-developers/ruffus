"""Regression tests for split decorator argument dispatch."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from uuid import uuid4

from ruffus import originate, pipeline_run, regex, split


class TestSplitKeywordArguments(unittest.TestCase):
    def test_split_argument_forms(self):
        for syntax in ('keywords', 'mixed', 'positional', 'legacy_regex'):
            with self.subTest(syntax=syntax), TemporaryDirectory() as directory:
                root = Path(directory)
                calls = []
                log = 'test log'
                context = {'setting': 42}

                def previous(outfile):
                    Path(outfile).write_text('input')

                def task_fn(infiles, outfiles, received_log, received_context):
                    self.assertEqual(received_log, log)
                    self.assertEqual(received_context, context)
                    calls.append('split')
                    (root / 'part.pdf').write_text('output')

                # Decorators register tasks in the shared main pipeline.
                previous.__name__ = 'previous_' + uuid4().hex
                task_fn.__name__ = 'split_' + uuid4().hex
                originate(str(root / 'input.txt'))(previous)
                output = str(root / '*.pdf')
                if syntax == 'keywords':
                    decorator = split(input=previous, output=output,
                                      extras=[log, context])
                elif syntax == 'mixed':
                    decorator = split(previous, output=output, extras=[log, context])
                elif syntax == 'positional':
                    decorator = split(previous, output, log, context)
                else:
                    decorator = split(previous, regex(r'.*\.txt$'), output, log, context)
                decorator(task_fn)
                options = dict(target_tasks=[task_fn], verbose=0, multiprocess=1,
                               history_file=str(root / 'history.sqlite'))
                pipeline_run(**options)
                pipeline_run(**options)
                self.assertEqual(calls, ['split'])
                self.assertEqual((root / 'part.pdf').read_text(), 'output')


if __name__ == '__main__':
    unittest.main()
