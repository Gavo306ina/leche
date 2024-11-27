from pymongo import MongoClient
from models import Productor, Proveedor, Leche, Pagas
#from chat import litros
from db import ConnectDB
import datetime

client = MongoClient(
    'mongodb+srv://nose:nose@nose.87wxfml.mongodb.net/?retryWrites=true&w=majority&appName=nose'
)

db = client['nose']
cole = db['leche']
doc = cole.find_one({})

address = doc['address']
user = Productor(name = doc['name'], email = doc['email'], phone = doc['phone'], password = doc['password']
                 , city = address['city'], street = address['street'], number = address['number'], plus_code = address['plus_code'])
#for doc in cole.find({}): # en la {} se puede escribir filtros o variables de busqueda
print(user, "\n")

proveedores = doc['proveedors']

for proveedor in proveedores:
    proveedor_address = proveedor['address']
    prove = Proveedor(name=proveedor['name'], email=proveedor['email'], proveedor_phone=proveedor['proveedor_phone'],
        city=proveedor_address['city'], street=proveedor_address['street'], number=proveedor_address['number'], plus_code=proveedor_address['plus_code']
    )
    print(prove)
    poga = proveedor['paga']
    litros = proveedor['litros']      
    litros_lista = []   
    paga_lista = []

    # Crear instancias de Leche a partir de los datos
    for datos in litros:
        leche_obj = Leche(litros_leche=datos['litros_leche'], fecha_leche=datos['fecha_leche'])
        litros_lista.append(leche_obj)
    # Mostrar todos los objetos de la lista
    for leche in litros_lista:
        print(leche)  
        
    for datos in poga:
        paga_obj = Pagas(litros_paga=datos['litros_paga'], monto_paga = datos['monto_paga'], fecha_paga=datos['fecha_paga'])
        paga_lista.append(paga_obj)

    # Mostrar todos los objetos de la lista
    for paga in paga_lista:
        print(paga)  
    
    