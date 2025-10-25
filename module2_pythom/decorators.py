import time
from decimal import Decimal


def timer(func):
    def wrapper():
        start_time = time.time()
        res = func()
        end_time = time.time() - start_time
        print(f"Execution time: {Decimal(end_time).quantize(Decimal('0.1'))}s")
        return res
    return wrapper


@timer
def just_func():
    time.sleep(1)


just_func()
