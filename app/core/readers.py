import os
import json
import csv
from app.core.mappings import get_catalunya_library, get_euskadi_library, get_valencian_library
from app.utils.utils import flatten_list, xml_to_json


catPath = os.path.join(os.path.dirname(__file__), "../static/catalunya.xml")
eusPath = os.path.join(os.path.dirname(__file__), "../static/euskadi.json")
valPath = os.path.join(os.path.dirname(__file__), "../static/valenciana.csv")


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
            res.append(get_euskadi_library(lib))
    return res


def get_catalan_libraries():
    with open(catPath, 'r', encoding='utf-8') as file:
        obj = xml_to_json(file.read())
        rows = obj['response']['row']
        res = []
        for lib in rows:
            res.append(get_catalunya_library(lib))
    return res


def get_valencian_librabries():
    data = []
    with open(valPath, "r", encoding='utf-8') as infile:
        reader = csv.DictReader(infile)  # read rows into a dictionary format
        elems = reader.fieldnames[0].split(';')
        for row in reader:
            values = ';'.join(flatten_list(list(row.values()))).split(';')
            data.append(get_valencian_library(values, elems))
    return data


def search_by(states):
    data = []
    for state in states:
        libs = get_library_from(state)
        data = data + libs
    return data