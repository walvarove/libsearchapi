from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.src.models import Library, LibraryType, Locality, Province, State


def get_libraries(db: Session, province_ids: Optional[List[int]] = [], locality_ids: Optional[List[int]] = [], states_ids: Optional[List[int]] = [], types: Optional[List[LibraryType]] = []):


    query = db.query(Library).join(Locality)

    if len(types):
        query = query.filter(Library.type.in_(types))

    if len(locality_ids):
        query = query.filter(Locality.id.in_(locality_ids))

    query = query.join(Province)

    if len(province_ids):
        query = query.filter(Province.id.in_(province_ids))

    query = query.join(State)

    if len(states_ids):
        query = query.filter(State.id.in_(states_ids))


    return query.all()


def get_library(db:Session, id: int):
    return db.query(Library).filter_by(id=id).first()
    
def get_location_info(db: Session):
    result = db.query(State).options(joinedload(State.provinces).
                                     subqueryload(Province.localities)).all()
    return result
