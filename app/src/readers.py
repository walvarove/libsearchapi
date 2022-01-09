import os
import json
import csv
from typing import List
from typing import Final

from selenium import webdriver
from app.src.mappers import map_catalunya_library, map_euskadi_library, map_valencian_library
from app.utils.utils import flatten_list, xml_to_json


catPath = os.path.join(os.path.dirname(__file__), "../static/catalunya.xml")
eusPath = os.path.join(os.path.dirname(__file__), "../static/euskadi.json")
valPath = os.path.join(os.path.dirname(__file__), "../static/valenciana.csv")

catPathDemo = os.path.join(os.path.dirname(__file__), "../static/cat-demo.xml")
eusPathDemo = os.path.join(os.path.dirname(__file__), "../static/eus-demo.json")
valPathDemo = os.path.join(os.path.dirname(__file__), "../static/val-demo.csv")



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


def get_library_from(state_slug: str):
    if state_slug == 'cat':
        return get_catalan_libraries()
    elif state_slug == 'val':
        return get_valencian_librabries()
    elif state_slug == 'eus':
        return get_eusaki_libraries()
    return []


def get_eusaki_libraries():
    res = []
    with open(eusPathDemo, encoding='utf-8') as file:
        libraries = json.load(file)
        for lib in libraries:
            res.append(map_euskadi_library(lib))
    return res


def get_catalan_libraries():
    res = []
    with open(catPathDemo, 'r', encoding='utf-8') as file:
        obj = xml_to_json(file.read())
        rows = obj['response']['row']
        for lib in rows:
            res.append(map_catalunya_library(lib))
    return res


def get_valencian_librabries():
    browser = runBrowser()
    res = []
    with open(valPathDemo, "r", encoding='utf-8') as infile:
        reader = csv.DictReader(infile)  # read rows into a dictionary format
        elems = reader.fieldnames[0].split(';')
        for row in reader:
            values = ';'.join(flatten_list(list(row.values()))).split(';')
            res.append(map_valencian_library(values, elems,browser))
    browser.close()
    return res

def runBrowser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-web-security") 
    chrome_options.add_argument('--disable-dev-shm-usage') 
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get('https://www.google.com/maps')
    browser.find_element_by_xpath('//*[@id="XmI62e"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form').click()
    return browser

