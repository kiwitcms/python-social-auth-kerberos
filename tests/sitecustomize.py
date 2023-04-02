# Enable Python coverage for subprocesses. See:
# http://nedbatchelder.com/code/coverage/subprocess.html
import os

os.environ.setdefault("COVERAGE_PROCESS_START", "/Kiwi/.coveragerc")

import coverage

coverage.process_startup()
