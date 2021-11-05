from collections import defaultdict
from posix import EX_SOFTWARE
from typing import List, Optional

import pandas as pd
from app.core.mappings import all_libs
from app.core.readers import search_by
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.models.library import Library, Locality, Province  # new
from app.db.session import engine  # new


def create_tables():  # new
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
