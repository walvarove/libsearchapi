from os import name
from posix import EX_SOFTWARE
from app.core.mappings import csv_to_json, xml_to_json, catPath, eusPath, valPath
from app.utils.utils import flatten_list
from fastapi import FastAPI
from app.core.config import settings
from app.db.session import engine  # new
from app.core.models.library import Library, Locality, Province  # new
from typing import Optional
import json
import pandas as pd
import csv
import io
from collections import defaultdict


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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api")
def return_api():
    return {"Hello": "api"}


@app.get("/cat")
def return_api():
    with open(catPath, 'r') as file:
        return xml_to_json(file.read())


@app.get("/eus")
def return_api():
    with open(eusPath, encoding='utf-8') as file:
        libraries = json.load(file)
        res = []
        for lib in libraries:
            res.append({
                'nombre': lib['documentName'],
                'description': lib['documentDescription'],
                'codigoPostal': lib['postalcode'].replace('.', ''),
                'longitud': lib['latwgs84'],
                'latitud': lib['lonwgs84'],
                'tipo': 'PU',
                'direccion': lib['address'],
                'email': lib['email'],
                'web': lib['webpage'],
                'localidad': {
                        'nombre': lib['municipality'],
                        'codigo': lib['municipalitycode']
                },
                'provincia': {
                    'nombre': lib['territory'],
                    'codigo': lib['territorycode']
                }
            })
    return res


@app.get("/val")
def return_api():
    data = []
    with open(valPath, "r", encoding='utf-8') as infile:
        reader = csv.DictReader(infile)  # read rows into a dictionary format
        elems = reader.fieldnames[0].split(';')
        for row in reader:
            flatList = flatten_list(list(row.values()))[0].split(';')
            print(flatList)
            stringList = ";".join(flatList)
            print(stringList)
            values = stringList.split(';')
            print(values)
            # MAPPING #
            iNombre = elems.index('NOMBRE')
            iDescription = elems.index('TIPO')
            iDireccion = elems.index('DIRECCION')
            iCodigoPostal = elems.index('CP')
            iTipo = elems.index('COD_CARACTER')
            iEmail = elems.index('EMAIL')
            iWeb = elems.index('WEB')
            iNombreMunicipio = elems.index('NOM_MUNICIPIO')
            iCodMunicipio = elems.index('COD_MUNICIPIO')
            iNombreProvincia = elems.index('NOM_PROVINCIA')
            iCodProvincia = elems.index('COD_PROVINCIA')
            data.append({
                'nombre': values[iNombre],
                'description': values[iDescription],
                'codigoPostal': values[iCodigoPostal],
                'tipo': values[iTipo],
                'direccion': values[iDireccion],
                'email': values[iEmail],
                'web': values[iWeb],
                'localidad': {
                    'nombre': values[iNombreMunicipio],
                    'codigo': values[iCodMunicipio]
                },
                'provincia': {
                    'nombre': values[iNombreProvincia],
                    'codigo': values[iCodProvincia]
                }
            })
    return data


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
