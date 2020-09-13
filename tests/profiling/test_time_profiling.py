import math

from profiling import time_profiling


def test_process_time():
    time_profiling.start()
    n = [math.sqrt(x) for x in range(100)]  # noqa: F841
    time_profiling.stop()
    result = time_profiling.get_result()
    assert "process_time" in result


def test_contexts():
    time_profiling.start()
    n = [math.sqrt(x) for x in range(100)]  # noqa: F841
    time_profiling.set_context("ab")
    time_profiling.set_context("a")
    a = [math.sqrt(x) for x in range(1000)]  # noqa: F841
    time_profiling.unset_context("a")
    time_profiling.set_context("b")
    b = [math.sqrt(x) for x in range(500)]  # noqa: F841
    time_profiling.unset_context("b")
    time_profiling.unset_context("ab")
    time_profiling.stop()
    result = time_profiling.get_result()
    assert "contexts" in result
    assert "a" in result["contexts"]
    assert "b" in result["contexts"]
    assert "ab" in result["contexts"]
    assert result["contexts"]["ab"] >= (result["contexts"]["a"] +
                                        result["contexts"]["b"])
    assert result["process_time"] >= result["contexts"]["ab"]
