from fastapi import Depends, FastAPI, Request, status
# from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from sqlalchemy.orm import Session
from pydantic import ValidationError

import src.models as models
import src.app.schemas as schemas
import src.app.crud as crud
from src.db import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# хэндлер по отлову ошибок десериализации
@app.exception_handler(ValidationError)
def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


@app.get('/chars/{char_id}', response_model=schemas.CharSchema)
def read_char(char_id: int, db: Session = Depends(get_db)):
    ans = crud.get_char_by_id(db, char_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({'detail': ans})
    )


@app.get('/towns/{town_id}', response_model=schemas.CharSchema)
def read_town(town_id: int, db: Session = Depends(get_db)):
    ans = crud.get_town_by_id(db, town_id)
    return ans


@app.get('/states/{state_id}', response_model=schemas.CharSchema)
def read_state(state_id: int, db: Session = Depends(get_db)):
    ans = crud.get_state_by_id(db, state_id)
    return ans


@app.get('/game/{game_id}', response_model=schemas.GameSchema)
def read_game(game_id: int, db: Session = Depends(get_db)):
    ans = crud.get_game_by_id(db, game_id)
    return ans


@app.post('/subEmail')
def read_email(item: schemas.MailModel):
    # save email
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({'detail': 'Thank you for sub!'})
    )