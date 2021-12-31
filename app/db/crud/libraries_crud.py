from typing import List
from sqlalchemy.orm import Session, joinedload
from app.src.models import Library, Locality, Province, State


def get_libraries(db: Session, province_ids: List[int], locality_ids: List[int], states_ids: List[int]):

    print(locality_ids)

    query = db.query(Library).join(Locality)

    if len(locality_ids):
        query = query.filter(Locality.id.in_(locality_ids))

    query = query.join(Province)

    if len(province_ids):
        query = query.filter(Province.id.in_(province_ids))

    query = query.join(State)

    if len(states_ids):
        query = query.filter(State.id.in_(states_ids))

    return query.all()


def get_location_info(db: Session):
    result = db.query(State).options(joinedload(State.provinces).
                                     subqueryload(Province.localities)).all()
    return result
