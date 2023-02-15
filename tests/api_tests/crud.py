from sqlalchemy.orm import Session

from src.models import Test


def test(
    db: Session,
    id: int
):
    return db.query(Test).filter(Test.id == id).first().__dict__
