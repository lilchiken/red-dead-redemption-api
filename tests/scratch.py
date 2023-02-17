import multiprocessing
import requests
import time
from functools import wraps


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} '
              f'{kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


alist = ['https://swapi.dev/api/people' for _ in range(100)]


# @timeit
# def without_mp():
#     for _ in alist:
#         requests.get(_)


# without_mp()


if __name__ == '__main__':
    with multiprocessing.Pool(multiprocessing.cpu_count() * 3) as p:
        @timeit
        def lalala():
            (p.map(requests.get, alist))
        lalala()
        p.close()
