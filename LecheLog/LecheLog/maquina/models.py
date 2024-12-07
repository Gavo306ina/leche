from django.db import models
from .estses import db

# Create your models here.

prod_col = db['leche']
#print(prod_col)


"""class Productor(models.Model):
    prod_id = models.AutoField(primary_key = True)
    prod_name = models.CharField(max_length = 150)
    prod_email = models.EmailField()
    prod_phone = models.CharField(max_length = 15)
    prod_password = models.CharField(max_length = 20)
    prod_city = models.CharField(max_length = 30)
    prod_street = models.CharField(max_length = 30)
    prod_number = models.IntegerField()
    prod_pluscode = models.CharField(max_length = 20)
"""
class Productor(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=150)
    prod_email = models.EmailField()
    prod_phone = models.CharField(max_length=15)
    prod_password = models.CharField(max_length=20)
    prod_address = models.JSONField()  # Campo JSON para la dirección

    class Meta:
        db_table = 'leche'

    def __str__(self):
        return self.prod_name


class Proveedor(models.Model):
    prov_id = models.AutoField(primary_key = True)
    prov_name = models.CharField(max_length = 150)
    prov_email = models.EmailField()
    prov_phone = models.CharField(max_length = 15)
    prov_city = models.CharField(max_length = 30)
    prov_street = models.CharField(max_length = 30)
    prov_number = models.IntegerField()
    prov_pluscode = models.CharField(max_length = 20)

class Leche(models.Model):
    leche_id = models.AutoField(primary_key = True)
    litros_leche = models.IntegerField()
    fecha_leche = models.DateTimeField()


class Pagas(models.Model):
    paga_id = models.AutoField(primary_key = True)
    litros_paga = models.IntegerField()
    fecha_paga = models.DateTimeField()
    monto_paga = models.IntegerField()


