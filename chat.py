from pymongo import MongoClient
from datetime import datetime

# Conectar a MongoDB
client = MongoClient('mongodb+srv://nose:nose@nose.87wxfml.mongodb.net/')
db = client['nose']
collection = db['leche']


def litros(proveedor_name, litros_nuevos):
    # Asegurarse de que 'litros' sea un array en el proveedor correspondiente
    resultado = collection.update_one(
        {"proveedors.name": proveedor_name},  # Buscar el proveedor por su nombre
        {
            "$setOnInsert": {
                "proveedors.$.litros": []  # Inicializar 'litros' como un array vacío si no existe
            }
        },
        upsert=True  # Crear el proveedor si no existe
    )

    # Ahora agregamos los nuevos litros
    resultado = collection.update_one(
        {"proveedors.name": proveedor_name},  # Buscar proveedor por nombre
        {
            "$push": {
                "proveedors.$.litros": {  # Usar $push para agregar un nuevo elemento a 'litros'
                    "litros_leche": litros_nuevos,
                    "fecha_leche": datetime.now()  # Fecha actual en formato UTC
                }
            }
        }
    )

    if resultado.modified_count > 0:
        print(f"Se actualizó el proveedor {proveedor_name} con {litros_nuevos} litros de leche.")
    elif resultado.upserted_id is not None:
        print(f"Se creó el proveedor {proveedor_name} con {litros_nuevos} litros de leche.")
    else:
        print(f"No se encontró el proveedor {proveedor_name} o no se actualizó.")


def paga(proveedor_name, litros_paga):
    resultado = collection.update_one(
        {"proveedors.name": proveedor_name}, 
        {
            "$setOnInsert": {
                "proveedors.$.paga": []  
            }
        },
        
        upsert=True  # Crear el proveedor si no existe
    )
    resultado = collection.update_one(
        {"proveedors.name": proveedor_name},  # Buscar proveedor por nombre
        {
            "$push": {
                "proveedors.$.paga": {  # Usar $push para agregar un nuevo elemento a 'paga'
                    "litros_paga": litros_paga,
                    "fecha_paga": datetime.now() ,
                    "monto_paga": litros_paga * 300
                }
            }
        }
    )
    if resultado.modified_count > 0:
        print(f"Se actualizó el proveedor {proveedor_name} con {litros_paga} litros pagados de leche.")
    elif resultado.upserted_id is not None:
        print(f"Se creó el proveedor {proveedor_name} con {litros_paga} litros pagados de leche.")
    else:
        print(f"No se encontró el proveedor {proveedor_name} o no se actualizó.")
