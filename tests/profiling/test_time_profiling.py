import math

from profiling import time_profiling


def test_process_time():
    time_profiling.start()
    a = [math.sqrt(x) for x in range(100)]  # noqa: F841
    time_profiling.stop()
    result = time_profiling.get_result()
    assert "process_time" in result
