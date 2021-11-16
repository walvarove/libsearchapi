import os
import json
import csv
from typing import List

from sqlalchemy.sql.expression import insert
from app.core.mappings import map_catalunya_library, map_euskadi_library, map_valencian_library
from app.core.models.library import Library, Locality, Province
from app.db.session import Session
from app.utils.utils import flatten_list, xml_to_json


catPath = os.path.join(os.path.dirname(__file__), "../static/catalunya.xml")
eusPath = os.path.join(os.path.dirname(__file__), "../static/euskadi.json")
valPath = os.path.join(os.path.dirname(__file__), "../static/valenciana.csv")


def get_provinces_from(list_with_duplicated_provinces):
    res = []
    for province in list_with_duplicated_provinces:
        if province not in res:
            res.append(province)

    return res


def get_localitites_from(list_with_duplicated_localities):
    res = []
    for locality in list_with_duplicated_localities:
        if locality not in res:
            res.append(locality)

    return res


def get_library_from(ccaa: str):
    if ccaa == 'cat':
        return get_catalan_libraries()
    elif ccaa == 'val':
        return get_valencian_librabries()
    elif ccaa == 'eus':
        return get_eusaki_libraries()
    return []


def get_eusaki_libraries():
    res = []
    with open(eusPath, encoding='utf-8') as file:
        libraries = json.load(file)
        for lib in libraries:
            res.append(map_euskadi_library(lib))
    return res


def get_catalan_libraries():
    res = []
    with open(catPath, 'r', encoding='utf-8') as file:
        obj = xml_to_json(file.read())
        rows = obj['response']['row']
        for lib in rows:
            res.append(map_catalunya_library(lib))
    return res


def get_valencian_librabries():
    res = []
    with open(valPath, "r", encoding='utf-8') as infile:
        reader = csv.DictReader(infile)  # read rows into a dictionary format
        elems = reader.fieldnames[0].split(';')
        for row in reader:
            values = ';'.join(flatten_list(list(row.values()))).split(';')
            res.append(map_valencian_library(values, elems))
    return res


def load_by(ccaa):
    libraries: List[Library] = []

    for ca in ccaa:
        caLibs = get_library_from(ca)
        libraries = libraries + caLibs

    provinces = get_provinces_from(
        list(map(lambda x: x['province'], libraries)))

    localities = get_localitites_from(
        list(map(lambda x: x['locality'], libraries)))

    for province in provinces:
        localities_per_province = list(
            filter(lambda x: x['code'][:2] == province['code'], localities))
        province = Province(province['name'], province['code'])
        with Session() as session:
            session.add(province)
            session.flush()
            for locality in localities_per_province:
                locality = Locality(
                    locality['name'], locality['code'], province.id)
                session.add(locality)
                session.flush()
                libraries_per_locality = list(map(lambda library: Library(library.get('name', None), library.get('type', None), library.get('address', None), library.get('postcalCode', None), library.get('longitude', None),
                                                             library.get('latitude', None), library.get('email', None), library.get('phoneNumber', None), library.get('description', None), locality.id, province.id), libraries))
                session.add_all(libraries_per_locality)
                session.commit()
    return libraries
