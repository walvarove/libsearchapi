from typing import List
from sqlalchemy.orm import Session
from app.src.models.library import Library

def get_libraries(db: Session, skip: int = 0, limit: int = 100):
    result = db.query(Library).offset(skip).limit(limit).all()
    return result