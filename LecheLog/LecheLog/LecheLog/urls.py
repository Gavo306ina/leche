"""
URL configuration for LecheLog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from maquina import views


urlpatterns = [
    path('', views.index, name='index'),  # Ruta predeterminada
    path('inicioSesion', views.inicioSesion, name='inicioSesion'),  # Ruta predeterminada
    path('registro', views.registro, name='registro'),  # Ruta predeterminada
    path('registrar/', views.registrar_productor, name='Registrar Productor'),  
    path('proveedores/', views.listar_proveedores, name='listar_proveedores'),# ver coleccion
    path('proveedores/agregar/', views.agregar_proveedor, name='listar_proveedores'),
    path('litros/', views.listar_litros, name='listar_litros'),
    path('pagos/', views.listar_pagos, name='listar_pagos'),
    path('proveedores/<str:proveedor_name>/agregar_litros/', views.agregar_litros, name='agregar_litros'),
    path('proveedores/<str:proveedor_name>/agregar_pago/', views.agregar_pago, name='agregar_pago'),
    path('proveedores/<str:proveedor_name>/', views.detalles_proveedor, name='detalles_proveedor'),
]
