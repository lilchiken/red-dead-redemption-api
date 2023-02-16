import unittest
from functools import wraps
import time
import requests

from sqlalchemy.orm import Session

from src.db import engine
from src.models import Test
from tests.api_tests import fastapi, flask
from tests.api_tests.schemas import TestSchema


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
            ses.bulk_save_objects(Test(test='test') for _ in range(10))
            ses.commit()
            cls.list_test = [x[0] for x in ses.query(Test.id).all()]
            cls.one_obj = cls.list_test[0]

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        with cls.session as ses:
            ses.query(Test).delete()
            ses.commit()
            ses.close()

    @timeit
    def test_all_obj_fastapi(self):
        for x in self.list_test:
            requests.get(f'http://127.0.0.1:8000/test/{x}').content
            # ans = ses.query(Test).filter(Test.id == x[0]).first().__dict__
            # print(TestSchema.parse_obj(ans).json())

    @timeit
    def test_one_obj_fastapi(self):
        requests.get(f'http://127.0.0.1:8000/test/{self.one_obj}').content

    @timeit
    def test_all_obj_flask(self):
        for x in self.list_test:
            requests.get(f'http://127.0.0.1:1234/test/{x}').content

    @timeit
    def test_one_obj_flask(self):
        requests.get(f'http://127.0.0.1:1234/test/{self.one_obj}').content
