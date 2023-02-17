import unittest
from functools import wraps
import time
import requests
import subprocess

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


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.session = Session(bind=engine)
        with cls.session as ses:
            ses.bulk_save_objects(Test(test='test') for _ in range(100))
            ses.commit()
            cls.list_test = [x[0] for x in ses.query(Test.id).all()]
            cls.one_obj = cls.list_test[0]
        subprocess.run(
            'pgrep -f "gunicorn" | xargs kill -9',
            shell=True
        )
        time.sleep(2)
        cls.flask = subprocess.Popen(
            "gunicorn -w 14 -b 127.0.0.1:5000 'tests.api_tests.flask:app' "
            "--log-level ERROR",
            shell=True
        )
        time.sleep(5)
        cls.fastapi = subprocess.Popen(
            "gunicorn tests.api_tests.fastapi:app --workers 10 --worker-class "
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
