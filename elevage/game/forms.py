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
        self.fields['male_rabbits'].label = f"Male rabbits (Price: {regle.male_rabbit_price}€ each)"

        self.fields['female_rabbits'].widget.attrs['min'] = 0
        self.fields['female_rabbits'].label = f"Female rabbits (Price: {regle.female_rabbit_price}€ each)"

        self.fields['foodLevel'].widget.attrs['min'] = 0
        self.fields['foodLevel'].label = f"Food level (Price: {regle.food_price}€/kg)"

        self.fields['cageNumber'].widget.attrs['min'] = 0
        self.fields['cageNumber'].label = f"Cages (Price: {regle.cage_price}€ each)"

        self.fields['money'].widget.attrs['min'] = 0
        self.fields['money'].widget.attrs['max'] = regle.budget_limit
        self.fields['money'].label = f"Money (Max budget: {regle.budget_limit}€)"
        
class Actions(forms.Form):
    male_rabbits_to_sell = forms.IntegerField(min_value=0, initial=0)
    female_rabbits_to_sell = forms.IntegerField(min_value=0, initial=0)
    food_to_buy = forms.IntegerField(min_value=0, initial=0)
    cages_to_buy = forms.IntegerField(min_value=0, initial=0)

    def __init__(self, *args, **kwargs):
        elevage = kwargs.pop('elevage', None)
        super().__init__(*args, **kwargs)
        regle = Regle.objects.first()

        if elevage:
            male_rabbits = elevage.individus.filter(sex='M', state__in=['present', 'pregnant'], age__gte=3).count()
            female_rabbits = elevage.individus.filter(sex='F', state__in=['present', 'pregnant'], age__gte=3).count()

            self.fields['male_rabbits_to_sell'].widget.attrs['max'] = male_rabbits
            self.fields['male_rabbits_to_sell'].label = f"Male rabbits to sell (Price: {regle.rabbit_sale_price}€ each)"  

            self.fields['female_rabbits_to_sell'].widget.attrs['max'] = female_rabbits
            self.fields['female_rabbits_to_sell'].label = f"Female rabbits to sell (Price: {regle.rabbit_sale_price}€ each)"  

        self.fields['food_to_buy'].widget.attrs['max'] = math.floor(elevage.money / regle.food_price)
        self.fields['food_to_buy'].label = f"Food to buy (Price: {regle.food_price}€/kg)" 

        self.fields['cages_to_buy'].widget.attrs['max'] = math.floor(elevage.money / regle.cage_price)
        self.fields['cages_to_buy'].label = f"Cages to buy (Price: {regle.cage_price}€ each)"