from typing import List
from app.src.readers import get_library_from, get_localitites_from, get_provinces_from
from app.src.models.library import Library, Locality, Province
from app.db.session import Session
from app.db.crud import libraries_crud

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

        libraries_per_province = list(filter(
            lambda library: library['postal_code'][:2] == province['code'], libraries))
        print(len(libraries_per_province))
        localities_codes_from_libraries = list(
            map(lambda lib: lib['locality']['code'], libraries_per_province))
        print(len(localities_codes_from_libraries))
        localities_per_province = list(
            filter(lambda locality: locality['code'] in localities_codes_from_libraries, localities))
        print(len(localities_per_province))
        province = Province(province['name'], province['code'])

        with Session() as session:
            session.add(province)
            session.flush()
            for locality in localities_per_province:
                loc_code = locality['code']
                locality = Locality(
                    locality['name'], locality['code'], province.id)
                session.add(locality)
                session.flush()
                libraries_per_locality = list(
                    filter(lambda lib: lib['locality']['code'] == loc_code, libraries_per_province))
                print(len(libraries_per_locality))
                libs = []
                for lib in libraries_per_locality:
                    libs.append(Library(lib['name'], lib['type'], lib['address'], lib['postal_code'], lib['longitude'],
                                lib['latitude'], lib['email'], lib['phone_number'], lib['description'], locality.id, province.id))
                session.add_all(libs)
                session.commit()
    return libraries_crud.get_libraries(session)
