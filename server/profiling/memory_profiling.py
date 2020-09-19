import tracemalloc

started = False

_current_context = None
_contexts_max_memory = {}


def start():
    global started, _contexts_max_memory, _current_context
    _contexts_max_memory = {}
    _current_context = None
    started = True


def set_context(context):
    global _current_context
    if _current_context is not None:
        raise RuntimeError("Cannot have multiple memory profiling contexts")
    _current_context = context
    tracemalloc.start()


def unset_context(context):
    global _current_context
    _current_context = None
    max_memory = tracemalloc.get_traced_memory()[1]
    if (context not in _contexts_max_memory
            or max_memory > _contexts_max_memory[context]):
        _contexts_max_memory[context] = max_memory
    tracemalloc.stop()


def stop():
    global started
    started = False


def get_result():
    return _contexts_max_memory
