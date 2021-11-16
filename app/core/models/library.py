from typing import Any, Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from pydantic import BaseModel
Base = declarative_base()


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
    # Relationships
    localities = relationship("Locality", back_populates="province")
    libraries = relationship("Library", back_populates="province")

    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code


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


class Library(Base):
    __name__ = 'locality'

    __tablename__: str = 'library'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    type = Column(String(255))
    address = Column(String(255))
    postalCode = Column(String(255))
    longitude = Column(String(255))
    latitude = Column(String(255))
    email = Column(String(255))
    phoneNumber = Column(String(255))
    description = Column(String(255))
    locality_id = Column(Integer, ForeignKey('locality.id'))
    province_id = Column(Integer, ForeignKey('province.id'))

    # Relationships
    locality = relationship("Locality", back_populates="libraries")
    province = relationship("Province", back_populates="libraries")

    def __init__(self: str, name: str, typing: str, address: str, postalCode: str, longitude: str, latitude: str, email: str, phoneNumber: str, description: str, locality_id: int, province_id: int):
        self.name = name
        self.type = typing
        self.address = address
        self.postalCode = postalCode
        self.longitude = longitude
        self.latitude = latitude
        self.email = email
        self.phoneNumber = phoneNumber
        self.description = description
        self.locality_id = locality_id
        self.province_id = province_id

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
    class Config:  
        orm_mode = True
class LibrarySchema(BaseModel):
    id: int
    name: str
    type: str
    address: Optional[str]
    postalCode: Optional[str]
    longitude: Optional[str]
    latitude: Optional[str]
    email: str
    phoneNumber: Optional[str]
    description: str
    locality_id: Optional[int]
    province_id: Optional[int]
    class Config:  
        orm_mode = True
