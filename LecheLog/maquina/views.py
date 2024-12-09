from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import prod_col
from .forms import ProductorForm, LitrosForm, PagaForm, ProveedorForm, LoginForm
from .estses import prod_col, db
from bson.objectid import ObjectId


def singout(request):
    # Cerrar la sesión
    logout(request)
    return redirect('inicio')

def singin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Verificar usuario en MongoDB
            user = db["leche"].find_one({"email": email, "password": password})

            if user:
                # Iniciar sesión creando una variable de sesión
                request.session['user_id'] = str(user['_id'])  # Guardar ID del usuario en la sesión
                request.session['user_name'] = user['name']  # Guardar el nombre del usuario en la sesión
                print(request.session.items())
                messages.success(request, f"¡Bienvenido, {user['name']}!")
                return redirect(teste)  # Redirigir a la página principal
            else:
                print("algo malo")
                messages.error(request, "Correo o contraseña incorrectos.")
    else:
        print("prueva")
        form = LoginForm()
    return render(request, 'inicioSesion.html', {'form': form})

def listar_proveedores(request):
    user_name = request.session.get('user_name')
    if not user_name:
        print("El usuario no está autenticado o el nombre de usuario no está en la sesión.")
        return redirect('login')  # O redirigir a una página de error o login si no hay 'user_name'

    # Filtrar los datos de MongoDB para obtener solo los productores del usuario
    cursor = db["leche"].find({"name" : user_name})
    
    # Convertir el cursor en una lista de diccionarios
    proveedores = []
    print(proveedores)
    for documento in cursor:
        if "proveedors" in documento:
            proveedores.extend(documento["proveedors"])
    # Pasar los datos a la plantilla
    return render(request, 'listaProveedores.html', {'proveedores': proveedores})

def detalles_proveedor(request, proveedor_name):
    # Verificar si el usuario ha iniciado sesión
    if 'user_name' not in request.session:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')  # Redirige a la vista de inicio de sesión si no hay sesión activa

    # Obtener el ID del usuario desde la sesión
    user_name = request.session.get('user_name')

    # Filtrar los datos de MongoDB para asegurar que solo se muestren los proveedores del usuario autenticado
    cursor = db["leche"].aggregate([
        {"$match": {"name" : user_name}},  # Filtrar por el ID del usuario
        {"$unwind": "$proveedors"},  # Separar los subdocumentos de los proveedores
        {"$match": {"proveedors.name": proveedor_name}},  # Filtrar por nombre del proveedor
        {"$project": {
            "litros": "$proveedors.litros",  # Extraer litros
            "paga": "$proveedors.paga",  # Extraer pagos
            "name": "$proveedors.name",
            "email": "$proveedors.email"
        }}
    ])

    # Convertir el cursor en una lista para procesarlo en la plantilla
    detalles = list(cursor)

    # Tomamos el primer elemento porque el proveedor es único
    detalles = detalles[0]
    return render(request, 'detalles.html', {'detalles': detalles, "user_name":user_name})


def listar_litros(request):
    # Obtener los litros de todos los proveedores
    litros = db["leche"].aggregate([
        {"$unwind": "$proveedors"},
        {"$unwind": "$proveedors.litros"},
        {"$project": {
            "litros_leche": "$proveedors.litros.litros_leche",
            "fecha_leche": "$proveedors.litros.fecha_leche"
        }}
    ])
    return render(request, 'LecheLog/litros.html', {'litros': litros})

def listar_pagos(request):
    # Obtener los pagos de todos los proveedores
    pagos = db["leche"].aggregate([
        {"$unwind": "$proveedors"},
        {"$unwind": "$proveedors.paga"},
        {"$project": {
            "litros_paga": "$proveedors.paga.litros_paga",
            "monto_paga": "$proveedors.paga.monto_paga",
            "fecha_paga": "$proveedors.paga.fecha_paga"
        }}
    ])
    return render(request, 'LecheLog/pagos.html', {'pagos': pagos})


def index(request):
    return render(request, 'inicio_O_registro.html')  # Renderiza la plantilla HTML

def registro(request):
    return render(request, 'LecheLog/registro.html')  # Renderiza la plantilla HTML

def agregar_litros(request, proveedor_name):
    if request.method == 'POST':
        form = LitrosForm(request.POST)
        if form.is_valid():
            litros = {
                "litros_leche": form.cleaned_data['litros_leche'],
                "fecha_leche": form.cleaned_data['fecha_leche']
            }
            # Actualizar el proveedor en MongoDB
            db["leche"].update_one(
                {"proveedors.name": proveedor_name},
                {"$push": {"proveedors.$.litros": litros}}
            )
            
            return redirect(listar_proveedores)
    else:
        form = LitrosForm()

    return render(request, 'LecheLog/litros.html', {'form': form, 'proveedor_name': proveedor_name})

def agregar_pago(request, proveedor_name):
    if request.method == 'POST':
        form = PagaForm(request.POST)
        if form.is_valid():
            pago = {
                "litros_paga": form.cleaned_data['litros_paga'],
                "monto_paga": form.cleaned_data['monto_paga'],
                "fecha_paga": form.cleaned_data['fecha_paga']
            }
            # Actualizar el proveedor en MongoDB
            db["leche"].update_one(
                {"proveedors.name": proveedor_name},
                {"$push": {"proveedors.$.paga": pago}}
            )
            return redirect(listar_proveedores)
    else:
        form = PagaForm()

    return render(request, 'LecheLog/paga.html', {'form': form, 'proveedor_name': proveedor_name})

def registrar_productor(request):
    if request.method == 'POST':
        form = ProductorForm(request.POST)
        if form.is_valid():
            # Crear el objeto del nuevo proveedor
            nuevo_productor = {
                "name": form.cleaned_data['name'],
                "email": form.cleaned_data['email'],
                "password": form.cleaned_data['password'],
                "phone": form.cleaned_data['phone'],
                "address": {
                    "street": form.cleaned_data['street'],
                    "number": form.cleaned_data['number'],
                    "city": form.cleaned_data['city'],
                    "plus_code": form.cleaned_data['plus_code']
                },
                "proveedors": []  # Inicia con una lista vacía
            }

            # Actualizar el documento del productor con el nuevo proveedor
            db["leche"].insert_one(nuevo_productor)

            # Redirigir a la lista de proveedores
            return redirect(index)
    else:
        form = ProductorForm()

    return render(request, 'contacto.html', {'form': form})

def agregar_proveedor(request):
    user_name = request.session.get('user_name')
    if not user_name:
        print("El usuario no está autenticado o el nombre de usuario no está en la sesión.")
        return redirect('login')  # O redirigir a una página de error o login si no hay 'user_name'

    print(user_name)

    # Filtrar los datos de MongoDB para obtener solo los productores del usuario
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            # Crear el objeto del nuevo proveedor
            nuevo_proveedor = {
                "name": form.cleaned_data['name'],
                "email": form.cleaned_data['email'],
                "proveedor_phone": form.cleaned_data['proveedor_phone'],
                "address": {
                    "street": form.cleaned_data['street'],
                    "number": form.cleaned_data['number'],
                    "city": form.cleaned_data['city'],
                    "plus_code": form.cleaned_data['plus_code']
                },
                "litros": [],  # Inicia con una lista vacía
                "paga": []  
            }

            # Actualizar el documento del productor con el nuevo proveedor
            db["leche"].update_one(
                {"name" : user_name}, 
                {"$push": {"proveedors": nuevo_proveedor}}  
            )

            # Redirigir a la lista de proveedores
            return redirect(listar_proveedores)
    else:
        form = ProveedorForm()

    return render(request, 'añadirReparto.html', {'form': form})

def teste(request):
    user_name = request.session.get('user_name')
    if not user_name:
        print("El usuario no está autenticado o el nombre de usuario no está en la sesión.")
        return redirect('login')  # O redirigir a una página de error o login si no hay 'user_name'

    print(user_name)

    # Conexión a MongoDB
    collection = db['leche']

    # Obtiene los datos de la colección
    repartos = collection.find_one({"name":user_name})

    proveedores = repartos.get('proveedors', [])

    entregas_por_mes = {}
    for proveedor in proveedores:
        for entrega in proveedor['litros']:
            fecha = entrega['fecha_leche']
            mes_anio = fecha.strftime("%B, %Y")  # Agrupa por mes y año

            if mes_anio not in entregas_por_mes:
                entregas_por_mes[mes_anio] = []

            entregas_por_mes[mes_anio].append({
                'proveedor': proveedor['name'],
                'litros': entrega['litros_leche'],
                'fecha': fecha.strftime("%d/%m/%Y"),
                'direccion': proveedor['address'],
                'telefono': proveedor['proveedor_phone'],
                'email': proveedor['email'],
                'pagos': proveedor.get('paga', [])
            })

    # Enviamos los datos al template
    return render(request, 'inicio.html', {'entregas_por_mes': entregas_por_mes})
    
    
#def testo(request):
 #   return render(request, 'LecheLog/registrosHistoricos.html')  # Renderiza la plantilla HTML
