from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.db import get_db
import tests.api_tests.schemas as schemas
import src.app.crud as crud

app = FastAPI()


@app.get('/chars/{game_id}', response_model=schemas.TestSchema)
def read_char(game_id: int, db: Session = Depends(get_db)):
    ans = crud.get_game_by_id(db, game_id)
    if not ans:
        return HTTPException(status_code=404, detail='Not Found')
    return ans
