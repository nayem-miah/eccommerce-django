from . models import *
from django import forms
from django_countries.widgets import CountrySelectWidget



class CheckoutForm(forms.Form):


    apartment_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Apartment address',
        'class': 'form-control',
        'required': True,
    }))
    country = CountryField(blank_label='Select country').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100',
        'required': True,
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': True,
    }))
