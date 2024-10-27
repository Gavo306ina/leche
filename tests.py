from pymongo import MongoClient
from models import Productor, Proveedor, Leche, Pagas
from db import ConnectDB
import datetime

client = MongoClient(
    'mongodb+srv://nose:nose@nose.87wxfml.mongodb.net/'
)

db = client['nose']
#print(db.list_collection_names())

cole = db['leche']

cole.insert_one(
    {
    "name":"El Lechero",
    "email":"adansanmartin.estudiante@gmail.com",
    "password":"123",
    "address":
        {"street":"Los Delfines",
         "number":"336",
         "city":"Calbuco",
         "plus_code":"6V84+HC6"
         },
    "phone":"+56 9 3745 7984",
    "proveedors":
        [
            {"name":"yo",
            "email":"gabriel.vidal12@inacapmail.cl",
            "proveedor_phone":"+56 9 3128 5774",
            "address":
                {"street":"Coyam",
                "number":None,
                "city":"Maullín",
                "plus_code":"CCX5+FRW"
                },
            "litros":{
                "litros_leche":34,
                "fecha_leche": datetime.datetime.now()
                },
            "paga":{
                "litros_paga":34,
                "fecha_paga": datetime.datetime.now(),
                "monto_paga": 1250
                }
            },
            {"name":"nose",
            "email":"menos",
            "proveedor_phone":None,
            "address":
                {"street":"Coyam",
                "number":None,
                "city":"Maullín",
                "plus_code":"CCV7+FW5"
                },
            "litros":{
                "litros_leche":75,
                "fecha_leche": datetime.datetime.now()
                },
            "paga":{
                "litros_paga":75,
                "fecha_paga": datetime.datetime.now(),
                "monto_paga": 7500
                }}
        ]

    }

)

doc = cole.find_one({})

address = doc['address']

user = Productor(name = doc['name'], email = doc['email'], phone = doc['phone'], password = doc['password']
                 , city = address['city'], street = address['street'], number = address['number'], plus_code = address['plus_code'])
#for doc in cole.find({}): # en la {} se puede escribir filtros o variables de busqueda
print(user, "\n\n")

proveedores = doc['proveedors']

for proveedor in proveedores:
    proveedor_address = proveedor['address']
    prove = Proveedor(name=proveedor['name'], email=proveedor['email'], proveedor_phone=proveedor['proveedor_phone'],
        city=proveedor_address['city'], street=proveedor_address['street'], number=proveedor_address['number'], plus_code=proveedor_address['plus_code']
    )
    poga = proveedor['paga']
    litros = proveedor['litros']
    pago = Pagas(litros_paga = poga['litros_paga'], monto_paga = poga['monto_paga'], fecha_paga = poga['fecha_paga'])
    litro = Leche(litros_leche = litros['fecha_leche'], fecha_leche = litros['fecha_leche'])
    print(prove, pago, litro)


