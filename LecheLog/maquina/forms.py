from django import forms
from .models import Productor

class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo Electrónico', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Correo Electrónico'
    }))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contraseña'
    }))

class ProductorForm(forms.Form):
    name = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nombre del Productor'
    }))
    email = forms.EmailField(label='Correo Electrónico', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Correo del Productor'
    }))
    password = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contraseña'
    }))


    phone = forms.CharField(label='Teléfono', max_length=15, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Teléfono (opcional)'
    }))
    street = forms.CharField(label='Calle', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Calle'
    }))
    number = forms.CharField(label='Número', max_length=10, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Número (opcional)'
    }))
    city = forms.CharField(label='Ciudad', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ciudad'
    }))
    plus_code = forms.CharField(label='Plus Code', max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Plus Code (opcional)'
    }))

class LitrosForm(forms.Form):
    litros_leche = forms.FloatField(label='Litros de Leche', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Cantidad de litros'
    }))
    fecha_leche = forms.DateTimeField(label='Fecha', widget=forms.DateInput(attrs={
        'type': 'datetime-local',
        'class': 'form-control',
    }))

class PagaForm(forms.Form):
    litros_paga = forms.FloatField(label='Litros Pagados', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Litros pagados'
    }))
    monto_paga = forms.FloatField(label='Monto Pagado', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Monto del pago'
    }))
    fecha_paga = forms.DateTimeField(label='Fecha', widget=forms.DateInput(attrs={
        'type': 'datetime-local',
        'class': 'form-control',
    }))

class ProveedorForm(forms.Form):
    name = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nombre del proveedor'
    }))
    email = forms.EmailField(label='Correo Electrónico', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Correo del proveedor'
    }))
    proveedor_phone = forms.CharField(label='Teléfono', max_length=15, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Teléfono (opcional)'
    }))
    street = forms.CharField(label='Calle', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Calle'
    }))
    number = forms.CharField(label='Número', max_length=10, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Número (opcional)'
    }))
    city = forms.CharField(label='Ciudad', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ciudad'
    }))
    plus_code = forms.CharField(label='Plus Code', max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Plus Code (opcional)'
    }))

