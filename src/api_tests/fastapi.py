from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.db import get_db
import schemas
import crud

app = FastAPI()


@app.get('/chars/{char_id}', response_model=schemas.CharSchema)
def read_char(char_id: int, db: Session = Depends(get_db)):
    ans = crud.get_char_by_id(db, char_id)
    if not ans:
        return HTTPException(status_code=404, detail='Not Found')
    return ans
