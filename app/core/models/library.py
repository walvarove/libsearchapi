from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Province:
    id: Any
    __name__: str

    def __init__(self, name: str, code: str):
        self.nombre = name
        self.codigo = code

    def __tablename__(cls) -> str:
        return cls.__name__.lower()

@as_declarative()
class Locality:
    id: Any
    __name__: str

    def __init__(self, name: str, code: str, province: Province):
        self.nombre = name
        self.codigo = code
        self.provincia = province

    def __tablename__(cls) -> str:
        return cls.__name__.lower()

@as_declarative()
class Library:
    id: Any
    __name__: str

    def __init__(self, name: str, type: str, address: str, zipcode: str, locality: Locality, longitud: str, latitud: str, email: str, phone: str, description: str):
        self.nombre = name
        self.tipo = type
        self.direccion = address
        self.codigoPostal = zipcode
        self.longitud = longitud
        self.latitud = latitud
        self.email = email
        self.telefono = phone
        self.descripcion = description
        self.localidad = locality

    def __tablename__(cls) -> str:
        return cls.__name__.lower()
