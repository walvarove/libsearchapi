from collections import defaultdict
from posix import EX_SOFTWARE
from typing import List, Optional

import pandas as pd
from app.core.mappings import all_libs
from app.core.readers import load_by, search_by
from fastapi import FastAPI, Query, status

from app.core.config import settings
from app.core.models.library import Base, Library, Locality, Province  # new
from app.db.session import Session, engine  # new


def create_tables():  # new
    with Session() as session:
        try: 
            session.query(Library).delete()
            session.query(Province).delete()
            session.query(Locality).delete()
            session.commit()
        except: 
            session.rollback()
    Library.metadata.create_all(bind=engine)
    Locality.metadata.create_all(bind=engine)
    Province.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,
                  version=settings.PROJECT_VERSION)

    create_tables()  # new
    return app


app = start_application()


@app.get("/search")
def search(state: List[str] = Query(all_libs)):
    states = state
    return search_by(states)


@app.get("/load", status_code=status.HTTP_204_NO_CONTENT)
def load(state: List[str] = Query(all_libs)):
    states = state
    return load_by(states)
