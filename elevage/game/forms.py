from django import forms
from .models import Elevage

class ElevageForm(forms.ModelForm):
    class Meta:
        model = Elevage
        fields = '__all__'
        exclude = ['month']