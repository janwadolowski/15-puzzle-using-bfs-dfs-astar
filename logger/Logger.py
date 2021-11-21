import functools
from datetime import datetime
from pathlib import Path
from time import time
from typing import Any


class Logger:
    def __init__(self, logfile: str):
        self.logfile = Path(logfile)

    def _write_log(self, msg: Any):
        with open(self.logfile, "a+") as f:
            f.write(str(msg))

    def TIME(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time()
            func_return = func(*args, **kwargs)
            end = time()
            timestamp = datetime.now().strftime("%H:%M:%S")
            self._write_log(
                f"[{timestamp}] {func.func_name} evaluated in {end - start} s."
            )

        func()
