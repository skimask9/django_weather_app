from django.forms import ModelForm
from django import forms
from .models import City

class CityForm(ModelForm):
    class Meta:
        model = City
        fields= ['name']
        labels = {
             'name':'',
         }
        widgets = {
            'name' :forms.TextInput(attrs={'class':'form-control', 'placeholder':'City Name'}),
            }