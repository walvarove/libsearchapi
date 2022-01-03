from typing import Any, List, Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Enum
from pydantic import BaseModel
Base = declarative_base()

class State(Base):
    __name__ = 'state'
    __tablename__: str = 'state'
    __table_args__ = (
        UniqueConstraint(
            'name', 'slug', name='state_name_slug_unique_constraint'),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    slug = Column(String(10))

    name_slug = {
        'eus': 'Euskadi',
        'cat': 'Cataluña',
        'val': 'Comunidad Valenciana'
    }
    
    # Relationships
    provinces = relationship("Province", back_populates="state")

    def __init__(self, slug: str):
        self.name = self.name_slug[slug]
        self.slug = slug


class Province(Base):
    __name__ = 'province'
    __tablename__: str = 'province'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    code = Column(String(2))
    __table_args__ = (
        UniqueConstraint(
            'name', 'code', name='province_name_code_unique_constraint'),
    )

    state_id = Column(Integer, ForeignKey("state.id"))

    # Relationships
    state = relationship("State", back_populates="provinces")
    localities = relationship("Locality", back_populates="province")

    def __init__(self, name: str, code: str, state_id: int):
        self.name = name
        self.code = code
        self.state_id = state_id

class Locality(Base):
    __name__ = 'locality'
    __tablename__: str = 'locality'
    __table_args__ = (
        UniqueConstraint(
            'name', 'code', name='locality_name_code_unique_constraint'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    code = Column(String(10))
    province_id = Column(Integer, ForeignKey("province.id"))
    
    # Relationships
    province = relationship("Province", back_populates="localities")
    libraries = relationship("Library", back_populates="locality")

    def __init__(self, name: str, code: str, province_id: int):
        self.name = name
        self.code = code
        self.province_id = province_id

class LibraryType(str, Enum):
    PUBLIC = 'PU'
    PRIVATE = 'PR'

class Library(Base):
    __name__ = 'locality'

    __tablename__: str = 'library'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    type: LibraryType = Column(String(255))
    address = Column(String(255))
    postal_code = Column(String(255))
    longitude = Column(String(255))
    latitude = Column(String(255))
    email = Column(String(255))
    phone_number = Column(String(255))
    description = Column(String(255))
    locality_id = Column(Integer, ForeignKey('locality.id'))

    # Relationships
    locality = relationship("Locality", back_populates="libraries")

    def __init__(self: str, name: str, type: LibraryType, address: str, postal_code: str, longitude: str, latitude: str, email: str, phone_number: str, description: str, locality_id: int):
        self.name = name
        self.type = type
        self.address = address
        self.postal_code = postal_code
        self.longitude = longitude
        self.latitude = latitude
        self.email = email
        self.phone_umber = phone_number
        self.description = description
        self.locality_id = locality_id


class LocalitySchema(BaseModel):
    id: int
    name: str
    code: str

    class Config:  
        orm_mode = True

class ProvinceSchema(BaseModel):
    id: int
    name: str
    code: str
    localities: List[LocalitySchema]

    class Config:  
        orm_mode = True

class LibrarySchema(BaseModel):
    id: int
    name: str
    type: LibraryType
    address: Optional[str]
    postal_code: Optional[str]
    longitude: Optional[str]
    latitude: Optional[str]
    email: str
    phone_number: Optional[str]
    description: str

    class Config:  
        orm_mode = True

class StateSchema(BaseModel):
    id: int
    name: str
    slug: str
    provinces: List[ProvinceSchema]

    class Config:  
        orm_mode = True