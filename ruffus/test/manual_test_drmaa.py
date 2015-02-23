from ruffus import *
from ruffus.drmaa_wrapper import *
import drmaa
drmaa_session = drmaa.Session()
drmaa_session.initialize()
logger, logger_mutex = cmdline.setup_logging ("me", "test.log", 1)
job_queue_name = "short.qb"
job_other_options='-P mott-flint.prjb'
run_job_using_drmaa ("ls", job_queue_name, None, "test_job_name", job_other_options, logger, drmaa_session)
