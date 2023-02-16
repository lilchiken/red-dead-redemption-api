from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.db import SessionLocal
import tests.api_tests.schemas as schemas
import tests.api_tests.crud as crud

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/test/{test}', response_model=schemas.TestSchema)
def read_char(test: int, db: Session = Depends(get_db)):
    ans = crud.test(db, test)
    if not ans:
        raise HTTPException(status_code=404, detail='Not Found')
    return ans
