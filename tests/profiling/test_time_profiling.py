import time

import pytest

from profiling import time_profiling


@pytest.fixture
def advance_timer(monkeypatch):
    current_time = 0

    def mocked_time():
        return current_time

    def advance(t):
        nonlocal current_time
        current_time += t

    monkeypatch.setattr(time, "process_time", mocked_time)
    return advance


def test_process_time(advance_timer):
    time_profiling.start()
    advance_timer(2)
    time_profiling.stop()
    result = time_profiling.get_result()
    assert result == {"process_time": 2, "contexts": {}}


def test_context(advance_timer):
    time_profiling.start()
    advance_timer(2)
    time_profiling.set_context("a")
    advance_timer(1)
    time_profiling.unset_context("a")
    advance_timer(1)
    time_profiling.stop()
    result = time_profiling.get_result()
    assert result == {"process_time": 4, "contexts": {"a": 1}}


def test_stop_unsetting_context(advance_timer):
    time_profiling.start()
    time_profiling.set_context("a")
    advance_timer(1)
    time_profiling.stop()
    result = time_profiling.get_result()
    assert result == {"process_time": 1, "contexts": {"a": 1}}


def test_overlapping_contexts(advance_timer):
    time_profiling.start()
    time_profiling.set_context("a")
    advance_timer(1)
    time_profiling.set_context("b")
    advance_timer(1)
    time_profiling.unset_context("a")
    time_profiling.unset_context("b")
    time_profiling.stop()
    result = time_profiling.get_result()
    assert result == {"process_time": 2, "contexts": {"a": 2, "b": 1}}


def test_profile_twice(advance_timer):
    time_profiling.start()
    time_profiling.set_context("a")
    advance_timer(2)
    time_profiling.unset_context("a")
    time_profiling.stop()

    time_profiling.start()
    time_profiling.set_context("a")
    advance_timer(1)
    time_profiling.unset_context("a")
    time_profiling.stop()

    result = time_profiling.get_result()
    assert result == {"process_time": 1, "contexts": {"a": 1}}
