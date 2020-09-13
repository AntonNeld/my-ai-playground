import gc
from time import process_time

time_before = None
time_after = None


def start():
    global time_before
    gc.disable()
    time_before = process_time()


def stop():
    global time_after
    time_after = process_time()
    gc.enable()


def get_result():
    return {"process_time": time_after - time_before}
