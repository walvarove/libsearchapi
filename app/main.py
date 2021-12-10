from collections import defaultdict
from posix import EX_SOFTWARE
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from fastapi import Depends, FastAPI, Query, status

from app.src.config import settings
from app.src.mappers import all_libs
from app.src.models.library import (Library, LibrarySchema,  # new
                                     Locality, Province)
from app.src.loaders import load_by
from app.db.crud import libraries_crud
from app.db.session import Session, engine  # new


# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def create_tables():  # new
    with Session() as session:
        try: 
            session.query(Library).delete()
            session.query(Locality).delete()
            session.query(Province).delete()
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
def search(db: Session = Depends(get_db)) -> List[LibrarySchema]:
    return libraries_crud.get_libraries(db)


@app.get("/load", status_code=status.HTTP_200_OK)
def load(ca: List[str] = Query(all_libs)):
    cas = ca
    return load_by(cas)
