from flask import Flask, abort
from sqlalchemy.orm import Session

from src.db import engine
import tests.api_tests.crud as crud

from src.models import Test
from tests.api_tests.schemas import TestSchema

app = Flask(__name__)

db = Session(bind=engine)


@app.route('/test/<test_id>')
def test(test_id: int):
    ans = crud.test(db, test_id)
    ans = TestSchema.parse_obj(ans).json()
    if not ans:
        return abort(404)
    return ans


@app.errorhandler(404)
def page_not_found(error):
    return {'bad': 'ans'}


if __name__ == '__main__':
    app.run(debug=True, port=1234)
