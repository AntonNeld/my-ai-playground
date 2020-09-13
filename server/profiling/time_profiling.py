import gc
from time import process_time

started = False

_time_before = None
_accumulated_time = None

_contexts_times_before = {}
_contexts_accumulated_time = {}


def start():
    global _time_before, _contexts_times_before, _accumulated_time
    global _contexts_accumulated_time, started
    gc.disable()
    _time_before = process_time()
    _contexts_times_before = {}
    _accumulated_time = None
    _contexts_accumulated_time = {}
    started = True


def set_context(context):
    _contexts_times_before[context] = process_time()


def unset_context(context):
    context_time = (process_time() - _contexts_times_before[context])
    if context not in _contexts_accumulated_time:
        _contexts_accumulated_time[context] = 0
    _contexts_accumulated_time[context] += context_time
    del _contexts_times_before[context]


def stop():
    global _accumulated_time, _time_before, started
    _accumulated_time = process_time() - _time_before
    _time_before = None
    gc.enable()
    started = False


def get_result():
    return {"process_time": _accumulated_time,
            "contexts": _contexts_accumulated_time}
