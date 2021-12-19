from collections import defaultdict
from posix import EX_SOFTWARE
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from fastapi import Depends, FastAPI, Query, status

from app.src.config import settings
from app.src.mappers import all_libs_slugs
from app.src.models import (Library, LibrarySchema, 
                                     Locality, Province, State)
from app.src.loaders import load_by
from app.db.crud import libraries_crud
from app.db.session import Session, engine


# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

def delete_tables():
    with Session() as session:
        try: 
            session.query(Library).delete()
            session.query(Locality).delete()
            session.query(Province).delete()
            session.query(State).delete()
            session.commit()
        except: 
            session.rollback()

def create_tables():  # new
    delete_tables();
    Library.metadata.create_all(bind=engine)
    Locality.metadata.create_all(bind=engine)
    Province.metadata.create_all(bind=engine)
    State.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,
                  version=settings.PROJECT_VERSION)

    create_tables()  # new
    return app

origins = ['*']


app = start_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search", response_model=List[LibrarySchema])
def search(state: List[str] = Query(all_libs_slugs), db: Session = Depends(get_db)) -> List[LibrarySchema]:
    states = state
    return libraries_crud.get_libraries(db, states)


@app.post("/load", status_code=status.HTTP_200_OK)
def load(state: List[str] = Query(all_libs_slugs)):
    states = state
    return load_by(states)

@app.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete():
    delete_tables()
    pass
