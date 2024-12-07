from django import forms
from .models import Productor

class ProductorForm(forms.ModelForm):
    class Meta:
        model = Productor
        fields = ['prod_name', 'prod_email', 'prod_phone', 'prod_password', 'prod_address']

    # Campos adicionales para la dirección (de forma individual)
    prod_street = forms.CharField(label='Calle', max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Calle',
    }))
    prod_number = forms.IntegerField(label='Número', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Número',
    }))
    prod_city = forms.CharField(label='Ciudad', max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ciudad',
    }))
    prod_pluscode = forms.CharField(label='Plus Code', max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Plus Code',
    }))

    def save(self, commit=True):
        # Combina los campos de dirección en prod_address
        instance = super().save(commit=False)
        instance.prod_address = {
            "prod_street": self.cleaned_data['prod_street'],
            "prod_number": self.cleaned_data['prod_number'],
            "prod_city": self.cleaned_data['prod_city'],
            "prod_pluscode": self.cleaned_data['prod_pluscode'],
        }
        if commit:
            instance.save()
        return instance

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

