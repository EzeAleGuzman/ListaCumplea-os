from django import forms
from .models import Cumpleañero

class CumpleañeroForm(forms.ModelForm):
    class Meta:
        model = Cumpleañero
        fields = '__all__' 
