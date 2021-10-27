import xmltodict
import json
import csv
import os
import pandas as pd

ValMAP = {
    "NOMBRE": 'nombre',
    "TIPO": 'descripcion',
    "DIRECCION": 'direccion',
    "CP": 'codigoPostal',
    "COD_CARACTER": 'tipo',
    "TELEFONO": 'telefono',
    "EMAIL": 'email',
    "WEB": 'web',
    "NOM_MUNICIPIO": 'nombre',
    "COD_MUNICIPIO:": 'codigo',
    "NOM_PROVINCIA": 'nombre',
    "COD_PROVINCIA:": 'codigo'
}

catPath = os.path.join(os.path.dirname(__file__), "../static/catalunya.xml")
eusPath = os.path.join(os.path.dirname(__file__), "../static/euskadi.json")
valPath = os.path.join(os.path.dirname(__file__), "../static/valenciana.csv")


def xml_to_json(input):
    obj = xmltodict.parse(input)
    return json.dumps(obj)


def csv_to_json(csvFile):
    return csvFile
