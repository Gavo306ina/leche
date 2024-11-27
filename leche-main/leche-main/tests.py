from pymongo import MongoClient
from models import Productor, Proveedor, Leche, Pagas
#from chat import litros
from db import ConnectDB
import datetime

client = MongoClient(
    'mongodb+srv://nose:nose@nose.87wxfml.mongodb.net/?retryWrites=true&w=majority&appName=nose'
)

db = client['nose']
#print(db.list_collection_names())

cole = db['leche']

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

