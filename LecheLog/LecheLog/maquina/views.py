from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import prod_col
from .forms import ProductorForm, LitrosForm, PagaForm, ProveedorForm
from .estses import prod_col, db


def listar_proveedores(request):
    # Obtener los proveedores desde MongoDB
    cursor = db["leche"].find({}, {"proveedors": 1, "_id": 0})
    
    # Convertir el cursor en una lista de diccionarios
    proveedores = []
    for documento in cursor:
        if "proveedors" in documento:
            proveedores.extend(documento["proveedors"])
    # Pasar los datos a la plantilla
    print(proveedores)
    return render(request, 'LecheLog/proveedor.html', {'proveedores': proveedores})

def detalles_proveedor(request, proveedor_name):
    # Buscar el proveedor específico por su nombre
    cursor = db["leche"].aggregate([
        {"$unwind": "$proveedors"},  # Separar los documentos en subdocumentos para cada proveedor
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
    
    if not detalles:
        return render(request, 'error.html', {'message': 'Proveedor no encontrado'})
    
    # Tomamos el primer elemento porque cada proveedor es único
    detalles = detalles[0]
    return render(request, 'LecheLog/detalles.html', {'detalles': detalles})


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


def registrar_productor(request):
    if request.method == 'POST':
        form = ProductorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(index)  # Redirige a una página de éxito
    else:
        form = ProductorForm()
        return render(request, 'LecheLog/form1.html', {'form': form})


def index(request):
    return render(request, 'LecheLog/index.html')  # Renderiza la plantilla HTML

def inicioSesion(request):
    return render(request, 'LecheLog/inicioSesion.html')  # Renderiza la plantilla HTML

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

def agregar_proveedor(request):
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
                {"name": 'El Lechero'}, 
                {"$push": {"proveedors": nuevo_proveedor}}  
            )

            # Redirigir a la lista de proveedores
            return redirect(listar_proveedores)
    else:
        form = ProveedorForm()

    return render(request, 'LecheLog/ag_proveedor.html', {'form': form})
