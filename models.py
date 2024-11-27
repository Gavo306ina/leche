#from pymongo import ConnectDB
import bcrypt
import datetime

class Productor:
    def __init__(self, name="", email="", phone = '',  password="", city="", street="", number="", plus_code=""):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.city = city
        self.number = number
        self.street = street
        self.plus_code = plus_code
        # Set dict type for mongodb
        self.user= {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "address":{
                "street": self.street,
                "number": self.number,
                "city": self.city,
                "plus_code": self.plus_code
            }
        }
        # Connect to MongoDB Usuarios Collection
        # self.userCollection = ConnectDB().get_conn().get_collection("leche")
                
    def exist(self):
        try:
            result =  self.userCollection.find_one({'email': self.email})
        except Exception as e:
            print("Error al verificar exitencia usuario:  ", e)
            result = e
        return True if result is not None else False

    def get(self):
        try:
            result = self.userCollection.find_one({'email': self.email})
        except Exception as e:
            print("Error al buscar usuario:  ", e)
            result = e
        return result if result is not None else None
    
    def save(self):
        if self.exist() == False:
            try:
                result = self.userCollection.insert_one(self.user)
            except Exception as e:
                print("Error al insertar usuario:  ", e)
                result = e
            return True if result.acknowledged == True else False
        else:
            return False

    def __str__(self):
        return f"""\tProductor\nName: {self.name} \nemail: {self.email} \npassword: {self.password} \ntelefono: {self.phone}
    \n\tDirección\nCalle: {self.street}\t\t Número: {self.number}\nCiudad: {self.city}\t\tPlus Code: {self.plus_code}"""


class Proveedor:
    def __init__(self, name="", email="",  proveedor_phone="", city="", street="", number="", plus_code=""):
        self.name = name
        self.email = email
        self.proveedor_phone = proveedor_phone
        self.city = city
        self.number = number
        self.street = street
        self.plus_code = plus_code
        # Set dict type for mongodb
        self.prover= {
            "name": self.name,
            "email": self.email,
            "proveedor_phone": self.proveedor_phone,
            "address":{
                "street": self.street,
                "number": self.number,
                "city": self.city,
                "plus_code": self.plus_code
            }
        }
    
    def __str__(self):
        return f"\n\n\tProveedor\nNombre: {self.name} \nEmail: {self.email} \tTelefono: {self.proveedor_phone}\n\tDirección\nCalle: {self.street}\t\t Número: {self.number}\nCiudad: {self.city}\t\tPlus Code: {self.plus_code}\n"
#user= Productor("test", "anpch@example.com", "123")
#print(user)

class Leche:
    def __init__(self, litros_leche = '', fecha_leche = ''):
        self.litros_leche = litros_leche
        self.fecha_leche = fecha_leche
        self.litros ={
                "litros_leche": self.litros_leche,
                "fecha_leche": self.fecha_leche
                }

    def __str__(self):
        return f"""\n\tDetalles de Leche\nFecha de Leche: {self.fecha_leche}\nLitros recogidos: {self.litros_leche}"""
    

class Pagas:
    def __init__(self, litros_paga = '', monto_paga = '', fecha_paga = ''):
        self.litros_paga = litros_paga
        self.monto_paga = monto_paga
        self.fecha_paga = fecha_paga
        self.paga ={
                "litros_leche_pagados": self.litros_paga,
                "fecha_paga": self.fecha_paga,
                "monto_paga": self.monto_paga
                }
        
    def __str__(self):
        return f"""\n\tDetalles de Pagos\nFecha de Paga: {self.fecha_paga}\nLitros pagados: {self.litros_paga}\nMonto Pagado: {self.monto_paga}"""
    


