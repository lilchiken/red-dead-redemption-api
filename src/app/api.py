from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import src.models as models
import src.app.schemas as schemas
import src.app.crud as crud
from src.db import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/chars/{char_id}', response_model=schemas.CharSchema)
def read_char(char_id: int, db: Session = Depends(get_db)):
    ans = crud.get_char_by_id(db, char_id)
    if not ans:
        return HTTPException(status_code=404, detail='Not Found')
    return ans