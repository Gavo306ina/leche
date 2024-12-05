from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import prod_col
from .forms import ProductorForm
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
    return render(request, 'LecheLog/nose.html', {'proveedores': proveedores})

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

def get_prod(request):
    prod =  prod_col.find_one({})
    return HttpResponse(prod)

def inicioSesion(request):
    return render(request, 'LecheLog/inicioSesion.html')  # Renderiza la plantilla HTML

def registro(request):
    return render(request, 'LecheLog/registro.html')  # Renderiza la plantilla HTML

