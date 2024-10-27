from pymongo import MongoClient

# Conectar a MongoDB
client = MongoClient('mongodb+srv://nose:nose@nose.87wxfml.mongodb.net/')
db = client['nose']
collection = db['leche']

# Nombre del proveedor que quieres buscar
nombre_proveedor = "yo"

# Consultar el documento que contiene el proveedor
documento = collection.find_one({'name': 'El Lechero'})  # Ajusta según necesites

# Verificar si se encontró el documento
if documento:
    print("Documento completo:", documento)  # Muestra todo el documento
    
    # Buscar el proveedor en la lista
    proveedor_encontrado = None
    for proveedor in documento.get('proveedors', []):
        if proveedor['name'] == nombre_proveedor:
            proveedor_encontrado = proveedor
            break
    
    # Mostrar los datos del proveedor si se encontró
    if proveedor_encontrado:
        print("Proveedor encontrado:")
        print("Nombre:", proveedor_encontrado['name'])
        print("Email:", proveedor_encontrado['email'])
        print("Teléfono del proveedor:", proveedor_encontrado['proveedor_phone'])
        
        # Acceder y mostrar la dirección
        direccion = proveedor_encontrado['address']
        print("Dirección del proveedor:")
        print("Calle:", direccion['street'])
        print("Número:", direccion['number'] if direccion['number'] is not None else "No disponible")
        print("Ciudad:", direccion['city'])
        print("Código plus:", direccion['plus_code'])
    else:
        print("Proveedor no encontrado.")
else:
    print("Documento no encontrado.")
