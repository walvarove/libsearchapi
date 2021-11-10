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

def get_library_from(state: str):
    if state == 'cat':
        return get_catalan_libraries()
    elif state == 'val':
        return get_valencian_librabries()
    elif state == 'eus':
        return get_eusaki_libraries()
    return []


def get_eusaki_libraries():
    with open(eusPath, encoding='utf-8') as file:
        libraries = json.load(file)
        res = []
        for lib in libraries:
            res.append(map_euskadi_library(lib))
    return res


def get_catalan_libraries():
    with open(catPath, 'r', encoding='utf-8') as file:
        obj = xml_to_json(file.read())
        rows = obj['response']['row']
        res = []
        for lib in rows:
            res.append(map_catalunya_library(lib))
    return res


def get_valencian_librabries():
    data = []
    with open(valPath, "r", encoding='utf-8') as infile:
        reader = csv.DictReader(infile)  # read rows into a dictionary format
        elems = reader.fieldnames[0].split(';')
        for row in reader:
            values = ';'.join(flatten_list(list(row.values()))).split(';')
            data.append(map_valencian_library(values, elems))
    return data


def search_by(states):
    data = []
    for state in states:
        libs = get_library_from(state)
        data = data + libs
    return data


def get_location_and_provinces():
    return {"locations:": [], "provinces": []}


def load_by(states):
    libsData: List[Library] = []

    for state in states:
        libs = get_library_from(state)
        libsData = libsData + libs

    provinces_flat = get_provinces_from(
        list(map(lambda x: x['province'], libsData)))
    provinces = list(map(lambda x: Province(
        name=x['name'], code=x['code']), provinces_flat))

    # localities_flat = get_localitites_from(
    #     list(map(lambda x: x['locality'], libsData)))
    # localities = list(map(lambda province: Locality(
    #     name=province.name, code=province.code, province=Province), provinces))

    with Session() as session:
        session.add_all(provinces)
        session.add_all(localities)
        session.commit()
    return get_provinces_from(provinces)
