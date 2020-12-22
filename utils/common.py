import time
import pickle
from loguru import logger as log
from .timetable import TimeTable

def timeExecute(method):
    def timed(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()
        log.info(
            "Time execution of '{}' function is: {} ms".format(
                method.__name__, (end - start) * 1000
            )
        )
        return result
    return timed

def loadTimeTable(path: str) -> TimeTable:
    with open(path, 'rb') as fd:
        return pickle.load(fd)
