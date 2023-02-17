import unittest
from functools import wraps
import time
import requests
import subprocess
import multiprocessing
import random

from sqlalchemy.orm import Session

from src.db import engine
from src.models import Test
# from tests.api_tests.schemas import TestSchema


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


def subprocrunShellTrue(cmd: str):
    return subprocess.run(cmd, shell=True)


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.session = Session(bind=engine)
        with cls.session as ses:
            ses.bulk_save_objects(Test(test='test') for _ in range(5))
            ses.commit()
            cls.list_test = [x[0] for x in ses.query(Test.id).all()]
            cls.one_obj = cls.list_test[0]
        cls.all_curl_flask = [f'curl -H "Accept: application/json" '
                              f'http://127.0.0.1:5000/test/{x}'
                              for x in cls.list_test]
        cls.all_curl_fastapi = [f'curl -H "Accept: application/json" '
                                f'http://127.0.0.1:8000/test/{x}'
                                for x in cls.list_test]
        cls.all_http_flask = [f'http://127.0.0.1:5000/test/{x}'
                              for x in cls.list_test]
        cls.all_http_fastapi = [f'http://127.0.0.1:8000/test/{x}'
                                for x in cls.list_test]
        subprocess.run(
            'pgrep -f "gunicorn" | xargs kill -9',
            shell=True
        )
        time.sleep(2)
        cls.flask = subprocess.Popen(
            "gunicorn -w 5 -b 127.0.0.1:5000 'tests.api_tests.flask:app' "
            "--log-level ERROR",
            shell=True
        )
        time.sleep(5)
        cls.fastapi = subprocess.Popen(
            "gunicorn tests.api_tests.fastapi:app --workers 5 --worker-class "
            "uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000 "
            "--log-level ERROR",
            shell=True
        )
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        with cls.session as ses:
            ses.query(Test).delete()
            ses.commit()
            ses.close()
        cls.fastapi.terminate()
        cls.flask.terminate()
        cls.fastapi.kill()
        cls.flask.kill()
        subprocess.run(
            'pgrep -f "gunicorn" | xargs kill -9',
            shell=True
        )

    @timeit
    def test_requests_all_obj_fastapi(self):
        for x in self.list_test:
            requests.get(f'http://127.0.0.1:8000/test/{x}').content

    @timeit
    def test_requests_one_obj_fastapi(self):
        requests.get(f'http://127.0.0.1:8000/test/{self.one_obj}').content

    @timeit
    def test_requests_all_obj_flask(self):
        for x in self.list_test:
            requests.get(f'http://127.0.0.1:5000/test/{x}').content

    @timeit
    def test_requests_one_obj_flask(self):
        requests.get(f'http://127.0.0.1:5000/test/{self.one_obj}').content

    @timeit
    def test_curl_one_obj_fastapi(self):
        subprocess.run(
            f'curl -H "Accept: application/json" '
            f'http://127.0.0.1:8000/test/{self.one_obj}', shell=True
        )

    @timeit
    def test_curl_one_obj_flask(self):
        subprocess.run(
            f'curl -H "Accept: application/json" '
            f'http://127.0.0.1:5000/test/{self.one_obj}', shell=True
        )

    @timeit
    def test_curl_all_obj_fastapi(self):
        for x in self.list_test:
            subprocess.run(
                f'curl -H "Accept: application/json" '
                f'http://127.0.0.1:8000/test/{x}', shell=True
            )

    @timeit
    def test_curl_all_obj_flask(self):
        for x in self.list_test:
            subprocess.run(
                f'curl -H "Accept: application/json" '
                f'http://127.0.0.1:5000/test/{x}', shell=True
            )

    def test_multiprocess(self):
        with multiprocessing.Pool(5) as pool:
            @timeit
            def multiprocess_test_fastapi_curls():
                pool.map(
                    subprocrunShellTrue,
                    self.all_curl_fastapi
                )
            multiprocess_test_fastapi_curls()

            @timeit
            def multiprocess_test_flask_curls():
                pool.map(
                    subprocrunShellTrue,
                    self.all_curl_flask
                )
            multiprocess_test_flask_curls()

            @timeit
            def multiprocess_test_fastapi_http():
                pool.map(
                    requests.get,
                    self.all_http_fastapi
                )
            multiprocess_test_fastapi_http()

            @timeit
            def multiprocess_test_flask_http():
                pool.map(
                    requests.get,
                    self.all_http_flask
                )
            multiprocess_test_flask_http()

            pool.close()

    def test_three_wrk(self):
        if len(self.list_test) <= 2:
            raise ValueError('Need to create more test rows (3 or more)')
        elif len(self.list_test) == 3:
            three_rndm_url = self.list_test.copy()
        else:
            three_rndm_url = []
            for _ in range(3):
                three_rndm_url.append(random.randint(
                    self.list_test[0], self.list_test[-1]
                ))
        for x in three_rndm_url:
            print('###FLASK###')
            subprocess.run(
                f'wrk -c100 -t5 -d10s http://127.0.0.1:5000/test/{x}',
                shell=True
            )
            print('###FASTAPI###')
            subprocess.run(
                f'wrk -c100 -t5 -d10s http://127.0.0.1:8000/test/{x}',
                shell=True
            )
