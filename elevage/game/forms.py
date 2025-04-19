from django import forms
from .models import Elevage, Regle
import math

class ElevageForm(forms.ModelForm):
    class Meta:
        model = Elevage
        fields = '__all__'
        exclude = ['month']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        regle = Regle.objects.first()
        
        self.fields['male_rabbits'].widget.attrs['min'] = 0
        self.fields['female_rabbits'].widget.attrs['min'] = 0
        self.fields['foodLevel'].widget.attrs['min'] = 0
        self.fields['cageNumber'].widget.attrs['min'] = 0
        self.fields['money'].widget.attrs['min'] = 0
        
        self.fields['money'].widget.attrs['max'] = regle.budget_limit
        
class Actions(forms.Form):
    def __init__(self, *args, **kwargs):
        elevage = kwargs.pop('elevage', None)
        super().__init__(*args, **kwargs)
        regle = Regle.objects.first()
        
        self.fields['male_rabbits_to_sell'].widget.attrs['max'] = elevage.male_rabbits
        self.fields['female_rabbits_to_sell'].widget.attrs['max'] = elevage.female_rabbits
        self.fields['food_to_buy'].widget.attrs['max'] = math.floor(elevage.money / regle.food_price)
        self.fields['cages_to_buy'].widget.attrs['max'] = math.floor(elevage.money / regle.cage_price)

    male_rabbits_to_sell = forms.IntegerField(min_value=0, initial=0)
    female_rabbits_to_sell = forms.IntegerField(min_value=0, initial=0)
    food_to_buy = forms.IntegerField(min_value=0, initial=0)
    cages_to_buy = forms.IntegerField(min_value=0, initial=0)