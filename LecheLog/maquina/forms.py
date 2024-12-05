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
