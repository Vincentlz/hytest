from .common import signal,GSTORE,INFO,STEP,CHECK_POINT,LOG_IMG,SELENIUM_LOG_SCREEN, CheckPointFail

import os, sys

def _ensure_cwd_first_in_syspath():
    cwd = os.path.abspath(os.getcwd())
    normalized_cwd = os.path.normcase(cwd)

    sys.path[:] = [
        path for path in sys.path
        if os.path.normcase(os.path.abspath(path or os.curdir)) != normalized_cwd
    ]
    sys.path.insert(0, cwd)


_ensure_cwd_first_in_syspath()
