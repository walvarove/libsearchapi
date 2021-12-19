from typing import List
from sqlalchemy.orm import Session
from app.src.mappers import all_libs_slugs
from app.src.models import Library, Locality, Province, State

def get_libraries(db: Session, states_slugs = all_libs_slugs):
    result = db.query(Library).join(Locality).join(Province).join(State).filter(State.slug.in_(states_slugs)).all()
    return result