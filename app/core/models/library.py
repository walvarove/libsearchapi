from typing import Any
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
Base = declarative_base()

# @as_declarative()
class Province(Base):
    __name__ = 'province'
    __tablename__:str = 'province'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    code = Column(String(2), unique=True)
    localities = relationship("Locality", back_populates="province")

# @as_declarative()
class Locality(Base):
    __name__ = 'locality'
    __tablename__: str = 'locality'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    code = Column(String(2), unique=True)
    province_id = Column(Integer, ForeignKey("province.id"))
    province = relationship("Province", back_populates="localities")
    libraries = relationship("Library", back_populates="locality")

# @as_declarative()
class Library(Base):
    __name__ = 'locality'

    __tablename__:str = 'library'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    tipo = Column(String(255))
    direccion = Column(String(255))
    codigoPostal = Column(String(255))
    longitud = Column(String(255))
    latitud = Column(String(255))
    email = Column(String(255))
    telefono = Column(String(255))
    descripcion = Column(String(255))
    locality_id = Column(Integer, ForeignKey('locality.id'))
    locality = relationship("Locality", back_populates="libraries")


