"""Exercise cluster retries without requiring a DRMAA installation or scheduler."""

from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from ruffus import drmaa_wrapper


class TestDrmaaRetries(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.directory = directory.name
        self.session = Mock()
        self.session.createJobTemplate.return_value = SimpleNamespace()
        self.session.runJob.side_effect = ["job-1", "job-2", "job-3"]
        for name, value in (
            ("gevent", SimpleNamespace(sleep=Mock())),
            ("drmaa", SimpleNamespace(JobState=SimpleNamespace(DONE="done", FAILED="failed"))),
        ):
            patcher = patch.object(drmaa_wrapper, name, value, create=True)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = patch.object(
            drmaa_wrapper, "read_stdout_stderr_from_files",
            return_value=(["output\n"], []),
        )
        self.read_output = patcher.start()
        self.addCleanup(patcher.stop)

    def run_job(self, resubmit):
        result = drmaa_wrapper.run_job_using_drmaa(
            "echo output", drmaa_session=self.session,
            job_script_directory=self.directory, resubmit=resubmit,
        )
        self.assertEqual(result, (["output\n"], []))
        self.read_output.assert_called_once()
        self.session.deleteJobTemplate.assert_called_once_with(
            self.session.createJobTemplate.return_value
        )
        self.assertEqual(list(Path(self.directory).iterdir()), [])

    def test_success_without_job_info_is_not_resubmitted(self):
        self.session.jobStatus.return_value = "done"
        self.run_job(resubmit=3)
        self.assertEqual(self.session.runJob.call_count, 1)

    def test_failure_is_retried_but_success_stops_retries(self):
        self.session.jobStatus.side_effect = ["failed", "done", "done"]
        self.run_job(resubmit=3)
        self.assertEqual(self.session.runJob.call_count, 2)

    def test_success_without_retries_submits_once(self):
        self.session.jobStatus.return_value = "done"
        self.run_job(resubmit=0)
        self.assertEqual(self.session.runJob.call_count, 1)

    def test_nonzero_exit_status_is_still_retried(self):
        failed = SimpleNamespace(exitStatus=1)
        succeeded = SimpleNamespace(
            exitStatus=0, resourceUsage={}, wasAborted=False,
            hasSignal=False, hasExited=True,
        )
        with patch.object(drmaa_wrapper, "submit_drmaa_job", side_effect=[
            ("job-1", failed), ("job-2", succeeded),
        ]) as submit:
            self.run_job(resubmit=3)
        self.assertEqual(submit.call_count, 2)


if __name__ == "__main__":
    unittest.main()
