from typing import List
from app.src.readers import get_library_from, get_localitites_from, get_provinces_from
from app.src.models import Library, Locality, Province, State
from app.db.session import Session
from app.db.crud import libraries_crud

def load_by(states_slugs):
    libraries: List[Library] = []
    state_ids = []
    
    for state_slug in states_slugs:
        caLibs = get_library_from(state_slug)
        libraries = libraries + caLibs

    with Session() as session:

        for state_slug in states_slugs:

            state = State(state_slug)
            session.add(state)
            session.flush()
            state_ids.append(state.id)

            provinces = get_provinces_from(
                list(map(lambda x: x['province'], list(filter(lambda x: x['state']['slug'] == state_slug,libraries)))))

            localities = get_localitites_from(
                list(map(lambda x: x['locality'], list(filter(lambda x: x['state']['slug'] == state_slug,libraries)))))


            for province in provinces:
                libraries_per_province = list(filter(
                lambda library: library['postal_code'][:2] == province['code'], libraries))
                localities_codes_from_libraries = list(
                map(lambda lib: lib['locality']['code'], libraries_per_province))
                localities_per_province = list(
                    filter(lambda locality: locality['code'] in localities_codes_from_libraries, localities))
                province = Province(province['name'], province['code'], state.id)

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
                    libs = []
                    for lib in libraries_per_locality:
                        libs.append(Library(lib['name'], lib['type'], lib['address'], lib['postal_code'], lib['longitude'],
                                    lib['latitude'], lib['email'], lib['phone_number'], lib['description'], locality.id))
                    session.add_all(libs)
        session.commit()
    return libraries_crud.get_libraries(session, [], [], state_ids)
