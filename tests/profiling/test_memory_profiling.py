import pytest
import tracemalloc

from profiling import memory_profiling


@pytest.fixture
def set_memory(monkeypatch):
    current_usage = 0
    peak_usage = 0

    def start():
        nonlocal current_usage, peak_usage
        current_usage = 0
        peak_usage = 0

    def stop():
        nonlocal current_usage, peak_usage
        current_usage = 0
        peak_usage = 0

    def mocked_memory():
        return (current_usage, peak_usage)

    def set(memory):
        nonlocal current_usage, peak_usage
        current_usage = memory
        if memory > peak_usage:
            peak_usage = memory

    monkeypatch.setattr(tracemalloc, "get_traced_memory", mocked_memory)
    monkeypatch.setattr(tracemalloc, "start", start)
    monkeypatch.setattr(tracemalloc, "stop", stop)
    return set


def test_context(set_memory):
    memory_profiling.start()
    set_memory(1000)
    set_memory(100)
    memory_profiling.set_context("a")
    set_memory(200)
    set_memory(100)
    memory_profiling.unset_context("a")
    memory_profiling.stop()
    result = memory_profiling.get_result()
    assert result == {"a": 200}


def test_only_one_context_allowed(set_memory):
    memory_profiling.start()
    memory_profiling.set_context("a")
    with pytest.raises(RuntimeError):
        memory_profiling.set_context("b")
    memory_profiling.stop()


def test_profile_twice(set_memory):
    memory_profiling.start()
    set_memory(1000)
    set_memory(100)
    memory_profiling.set_context("a")
    set_memory(200)
    set_memory(100)
    memory_profiling.unset_context("a")
    memory_profiling.set_context("b")
    set_memory(300)
    set_memory(400)
    memory_profiling.unset_context("b")
    memory_profiling.set_context("a")
    set_memory(100)
    memory_profiling.unset_context("a")
    memory_profiling.stop()
    result = memory_profiling.get_result()
    assert result == {"a": 200, "b": 400}
