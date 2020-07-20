from collections import OrderedDict
from functools import wraps
import time

from testandconquer import logger


total_time_by_function = OrderedDict()


def trace(wrapped):

    @wraps(wrapped)
    def decorated(*args, **kwargs):
        start_time = time.time()

        # run the wrapped function
        ret = wrapped(*args, **kwargs)

        func_name = wrapped.__name__
        duration = time.time() - start_time
        if func_name in total_time_by_function:
            total_time_by_function[func_name] += duration
        else:
            total_time_by_function[func_name] = duration

        if duration > 0.1:
            logger.info('⬆ %s took %s seconds', wrapped.__name__, duration)

        return ret

    return decorated


def print_summary():
    logger.info('Tracer Summary:')
    for k, v in total_time_by_function.items():
        logger.info('∑ func %s: %s', k, v)
