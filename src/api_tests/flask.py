from flask import Flask, abort

from src.db import get_db
import crud

app = Flask()


@app.route('/chars/{char_id}')
def read_char(char_id: int):
    ans = crud.get_char_by_id(get_db, char_id)
    if not ans:
        return abort(404)
    return ans


@app.errorhandler(404)
def page_not_found(error):
    return {'bad': 'ans'}
