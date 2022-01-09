import csv
import json
import time
from typing import Final

import pandas as pd
import xmltodict
from app.src.models import LibraryType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

all_libs_slugs: Final = ['cat', 'val', 'eus']


def get_type_cat(category: str):
    return LibraryType.PUBLIC if 'Públiques' in category else LibraryType.PRIVATE


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
        'postal_code': str(lib['cpostal']),
        'longitude': lib['longitud'],
        'latitude': lib['latitud'],
        'type': get_type_cat(lib['categoria']),
        'address': lib['via'],
        'email': lib['email'],
        'phone_number': lib['telefon1'] if 'telefon1' in lib else None,
        # 'web': lib['weburl'],
        'locality': {
            'name': lib['poblacio'],
            'code': lib['codi_municipi'][:5],
        },
        'province': {
            'name': get_provincia_cat(lib['cpostal']),
            'code': str(lib['cpostal'])[0:2]
        },
        'state': {
            'name': 'Cataluña',
            'slug': 'cat'
        }
    }


def map_euskadi_library(lib):
    postal_code = lib['postalcode'].replace('.', '')
    return {
        'name': lib['documentName'],
        'description': lib['documentDescription'],
        'postal_code': postal_code,
        'longitude': lib['lonwgs84'],
        'latitude': lib['latwgs84'],
        'type': LibraryType.PUBLIC,
        'address': lib['address'],
        'email': lib['email'],
        'web': lib['webpage'],
        'phone_number': lib['phone'],
        'locality': {
            'name': lib['municipality'],
            'code': postal_code
        },
        'province': {
            'name': lib['territory'],
            'code': postal_code[:2],
        },
        'state': {
            'name': 'Euskadi',
            'slug': 'eus'
        }
    }


def map_valencian_library(lib, elems, browser):
    i_name = elems.index('NOMBRE')
    i_description = elems.index('TIPO')
    i_address = elems.index('DIRECCION')
    i_postal_code = elems.index('CP')
    i_type = elems.index('COD_CARACTER')
    i_email = elems.index('EMAIL')
    i_web = elems.index('WEB')
    i_phone_number = elems.index('TELEFONO')
    i_locality_name = elems.index('NOM_MUNICIPIO')
    i_locality_code = elems.index('COD_MUNICIPIO')
    i_province_name = elems.index('NOM_PROVINCIA')
    i_province_code = elems.index('COD_PROVINCIA')
    adrs = str(lib[i_address])
    adrs = f'{adrs} {lib[i_postal_code]}'
    lag_lng = get_lag_lang_from_browser(browser, adrs)

    return {
        'name': lib[i_name],
        'description': lib[i_description],
        'postal_code': lib[i_postal_code].zfill(5),
        'longitude': lag_lng["long"],
        'latitude': lag_lng["lat"],
        'type': lib[i_type],
        'address': lib[i_address],
        'email': lib[i_email],
        'web': lib[i_web],
        'phone_number': lib[i_phone_number][5:],
        'locality': {
            'name': lib[i_locality_name].lower().title(),
            'code': lib[i_locality_code],
        },
        'province': {
            'name': lib[i_province_name].lower().title(),
            'code': lib[i_province_code].zfill(2)
        },
        'state': {
            'name': 'Comunidad valenciana',
            'slug': 'val'
        }
    }


def get_lag_lang_from_browser(browser, address):
    urladd = f'https://www.google.com/maps/search/{address}'
    browser.get(urladd)
    
    wait = WebDriverWait(browser, 10)
    wait.until(lambda driver: '@' in driver.current_url)
        

    res = browser.current_url
    res = str(res)
    res = res.split('@')
    res = res[1][:21]
    res = res.split(',')


    return {
        "lat": res[0],
        "long": res[1]
    }

