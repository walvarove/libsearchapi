from typing import Final
import xmltodict
from selenium import webdriver
import json
import csv
import pandas as pd
import time

all_libs: Final = ['cat', 'val', 'eus']

res = {
    "long" : '',
    "lat": '',
}

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


def map_valencian_library(lib, elems,browser):
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
    adrs = str(lib[iAddress])
    adrs = f'{adrs} {lib[iPostalCode]}'
    print('huelemelo cabron : ', adrs)
        
    res = runSearch(browser,adrs)
    return {
        'name': lib[iName],
        'description': lib[iDescription],
        'postalCode': lib[iPostalCode],
        'longitude':res["long"],
        'latitude':res["lat"],
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

def runSearch(browser,address):
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
    print('huele huele :',urladd)
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

 
