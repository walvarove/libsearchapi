from typing import Final
import xmltodict
import json
import csv
import pandas as pd

all_libs: Final = ['cat', 'val', 'eus']


def get_type_cat(str: str):
    obj = ''.join(reversed(str)).split('|')
    return ''.join(reversed(obj[0]))


def get_provincia_cat(str: str):
    if(str.startswith('43')):
        return 'Tarragona'
    elif str.startswith('08'):
        return 'Barcelona'
    elif str.startswith('17'):
        return 'Girona'
    elif str.startswith('25'):
        return 'Lleida'
    else:
        return 'Unknown Province'


def map_catalunya_library(lib):
    return {
        'name': lib['nom'],
        'description': lib['alies'],
        'postalCode': str(lib['cpostal']),
        'longitude': lib['longitud'],
        'latitude': lib['latitud'],
        'type': get_type_cat(str(lib['propietats'])),
        'address': lib['via'],
        'email': lib['email'],
        'phoneNumber': lib['telefon1'] if 'telefon1' in lib else None,
        # 'web': lib['weburl'],
        'locality': {
            'name': lib['poblacio'],
            'code': lib['codi_municipi'],
            'cpostal': str(lib['cpostal'])[:2]
        },
        'province': {
            'name': get_provincia_cat(lib['cpostal']),
            'code': str(lib['cpostal'])[0:2]
        }
    }


def map_euskadi_library(lib):
    postalCode = lib['postalcode'].replace('.', '')
    return {
        'name': lib['documentName'],
        'description': lib['documentDescription'],
        'postalCode': postalCode,
        'longitude': lib['latwgs84'],
        'latitude': lib['lonwgs84'],
        'type': 'PU',
        'address': lib['address'],
        'email': lib['email'],
        'web': lib['webpage'],
        'phoneNumber':lib['phone'],
        'locality': {
            'name': lib['municipality'],
            'code': postalCode[2:],
            'cpostal': postalCode
        },
        'province': {
            'name': lib['territory'],
            'code': postalCode[:2]
        }
    }


def map_valencian_library(lib, elems):
    iName = elems.index('NOMBRE')
    iDescription = elems.index('TIPO')
    iAddress = elems.index('DIRECCION')
    iPostalCode = elems.index('CP')
    iType = elems.index('COD_CARACTER')
    iEmail = elems.index('EMAIL')
    iWeb = elems.index('WEB')
    iPhoneNumber = elems.index('TELEFONO')
    iLocalityName = elems.index('NOM_MUNICIPIO')
    iLocalityCode = elems.index('COD_MUNICIPIO')
    iProvinceName = elems.index('NOM_PROVINCIA')
    iProvinceCode = elems.index('COD_PROVINCIA')
    return {
        'name': lib[iName],
        'description': lib[iDescription],
        'postalCode': lib[iPostalCode],
        'longitude':'',
        'latitude':'',
        'type': lib[iType],
        'address': lib[iAddress],
        'email': lib[iEmail],
        'web': lib[iWeb],
        'phoneNumber':lib[iPhoneNumber][5:],
        'locality': {
            'name': lib[iLocalityName].lower().title(),
            'code': lib[iLocalityCode],
            'cpostal':lib[iPostalCode]
        },
        'province': {
            'name': lib[iProvinceName].lower().title(),
            'code': lib[iProvinceCode]
        }
    }
