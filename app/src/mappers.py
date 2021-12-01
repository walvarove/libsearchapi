from typing import Final
import xmltodict
from selenium import webdriver
import json
import csv
import pandas as pd
import time

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
        'postal_code': str(lib['cpostal']),
        'longitude': lib['longitud'],
        'latitude': lib['latitud'],
        'type': get_type_cat(str(lib['propietats'])),
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
        'type': 'PU',
        'address': lib['address'],
        'email': lib['email'],
        'web': lib['webpage'],
        'phone_number':lib['phone'],
        'locality': {
            'name': lib['municipality'],
            'code': postal_code[2:]
        },
        'province': {
            'name': lib['territory'],
            'code': postal_code[:2]
        }
    }


def map_valencian_library(lib, elems,browser):
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
        
    lag_lng = get_lag_lang_from_browser(browser,adrs)

    return {
        'name': lib[i_name],
        'description': lib[i_description],
        'postal_code': lib[i_postal_code].zfill(5),
        'longitude':lag_lng["long"],
        'latitude':lag_lng["lat"],
        'type': lib[i_type],
        'address': lib[i_address],
        'email': lib[i_email],
        'web': lib[i_web],
        'phone_number':lib[i_phone_number][5:],
        'locality': {
            'name': lib[i_locality_name].lower().title(),
            'code': lib[i_locality_code],
        },
        'province': {
            'name': lib[i_province_name].lower().title(),
            'code': lib[i_province_code].zfill(2)
        }
    }

def get_lag_lang_from_browser(browser,address):
    # browser.execute_script("window.scrollTo(0,300)")
    # browser.find_element_by_xpath('//*[@id="address"]').clear()
    # browser.find_element_by_xpath('//*[@id="address"]').send_keys(address)
    # browser.save_screenshot('screen.png')
    # browser.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[3]/div[1]/form[1]/div[2]/div/button').click()
    # time.sleep(3)
    # res1 = browser.find_element_by_xpath('//*[@id="longitude"]').get_attribute('value')
    # res2 = browser.find_element_by_xpath('//*[@id="latitude"]').get_attribute('value')
    
    urladd = f'https://www.google.com/maps/place/{address}'
    browser.get(urladd)
    time.sleep(5)
    res = browser.current_url
    res = str(res)
    res = res.split('@')
    res = res[1][:21]
    res = res.split(',')
    return {
        "lat":res[0],
        "long":res[1]
    }

 
