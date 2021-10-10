class Province:
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code
        
class Locality:
    def __init__(self, name: str, code: str, province: Province):
        self.name = name
        self.code = code
        self.province = province
        
class Library:
    def __init__(self, name: str, type: str, address: str, zipcode: str, locality: Locality, longitud: str, latitud: str, email: str, phone: str, description: str):
        self.name = name
        self.type = type
        self.address = address
        self.zipcode = zipcode
        self.longitud = longitud
        self.latitud = latitud
        self.email = email
        self.phone = phone
        self.description = description
        self.locality = locality

        