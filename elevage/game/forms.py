from django import forms
from .models import Elevage

class ElevageForm(forms.ModelForm):
    class Meta:
        model = Elevage
        fields = '__all__'
        exclude = ['month']
        
class Actions(forms.Form):
    def __init__(self, *args, **kwargs):
        elevage = kwargs.pop('elevage', None)
        super().__init__(*args, **kwargs)
        if elevage:
            self.fields['male_rabbits_to_sell'].widget.attrs['max'] = elevage.male_rabbits
            self.fields['female_rabbits_to_sell'].widget.attrs['max'] = elevage.female_rabbits
            self.fields['food_to_buy'].widget.attrs['max'] = elevage.money 
            self.fields['cages_to_buy'].widget.attrs['max'] = elevage.money 

    male_rabbits_to_sell = forms.IntegerField(min_value=0, initial=0)
    female_rabbits_to_sell = forms.IntegerField(min_value=0, initial=0)
    food_to_buy = forms.IntegerField(min_value=0, initial=0)
    cages_to_buy = forms.IntegerField(min_value=0, initial=0)