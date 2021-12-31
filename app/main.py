from collections import defaultdict
from posix import EX_SOFTWARE
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from fastapi import Depends, FastAPI, Query, status

from app.src.config import settings
from app.src.mappers import all_libs_slugs
from app.src.models import (Library, LibrarySchema,
                            Locality, Province, State, StateSchema)
from app.src.loaders import load_by
from app.db.crud import libraries_crud
from app.db.session import Session, engine
from fastapi.openapi.utils import get_openapi


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

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
app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/libraries", response_model=List[LibrarySchema])
def libraries(locality_id: Optional[List[int]] = Query([]), province_id: Optional[List[int]] = Query([]), state_id: Optional[List[int]] = Query([]), db: Session = Depends(get_db)) -> Optional[List[LibrarySchema]]:
    return libraries_crud.get_libraries(db, province_id, locality_id, state_id)


@app.get("/locations", response_model=List[StateSchema])
def locations(db: Session = Depends(get_db)):
    return libraries_crud.get_location_info(db)


@app.post("/load", status_code=status.HTTP_200_OK)
def load(state: List[str] = Query(all_libs_slugs)):
    states = state
    return load_by(states)


@app.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete():
    delete_tables()
    pass
