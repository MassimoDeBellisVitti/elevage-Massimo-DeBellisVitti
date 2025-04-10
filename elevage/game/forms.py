from django import forms
from .models import Elevage

class ElevageForm(forms.ModelForm):
    class Meta:
        model = Elevage
        fields = '__all__'
        exclude = ['month']
        
class Actions(forms.Form):
    male_rabbits_to_sell = forms.IntegerField(min_value=0, initial=0)
    female_rabbits_to_sell = forms.IntegerField(min_value=0, initial=0)
    food_to_buy = forms.IntegerField(min_value=0, initial=0)
    cages_to_buy = forms.IntegerField(min_value=0, initial=0)