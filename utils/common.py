import time
from loguru import logger as log


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
