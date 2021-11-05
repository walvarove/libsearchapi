from typing import Final
import xmltodict
import json
import csv
import pandas as pd

all_libs: Final = ['cat','val','eus']

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
        return 'Provincia Random'



def get_catalunya_library(lib):
    return {
        'nombre': lib['nom'],
        'description': lib['alies'],
        'codigoPostal': lib['cpostal'],
        'longitud': lib['longitud'],
        'latitud': lib['latitud'],
        'tipo': get_type_cat(str(lib['propietats'])),
        'direccion': lib['via'],
        'email': lib['email'],
        # 'web': lib['weburl'],
        'localidad': {
            'nombre': lib['poblacio'],
            'codigo': lib['codi_municipi']
        },
        'provincia': {
            'nombre': get_provincia_cat(lib['cpostal']),
            'codigo': str(lib['cpostal'])[0:2]
        }
    }


def get_euskadi_library(lib):
    return {
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
    }


def get_valencian_library(lib, elems):
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
    return {
        'nombre': lib[iNombre],
        'description': lib[iDescription],
        'codigoPostal': lib[iCodigoPostal],
        'tipo': lib[iTipo],
        'direccion': lib[iDireccion],
        'email': lib[iEmail],
        'web': lib[iWeb],
        'localidad': {
            'nombre': lib[iNombreMunicipio],
            'codigo': lib[iCodMunicipio]
        },
        'provincia': {
            'nombre': lib[iNombreProvincia],
            'codigo': lib[iCodProvincia]
        }
    }


