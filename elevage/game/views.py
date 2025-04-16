from django.shortcuts import render, redirect, get_object_or_404
from .models import Elevage, Individu, Regle
from .forms import ElevageForm, Actions
from .services import update_food_and_advance_month

def nouveau(request):
    if request.method == 'POST':
        form = ElevageForm(request.POST)
        if form.is_valid():
            elevage = form.save()

            for _ in range(int(request.POST.get('male_rabbits', 0))):
                Individu.objects.create(elevage=elevage, sex='M', age=1)

            for _ in range(int(request.POST.get('female_rabbits', 0))):
                Individu.objects.create(elevage=elevage, sex='F', age=1)

            return redirect('elevage_detail', id=elevage.id)
    else:
        form = ElevageForm()
    return render(request, 'game/nouveau.html', {'form': form})

def elevage_list(request):
    elevages = Elevage.objects.all()
    return render(request, 'game/elevage_list.html', {'elevages': elevages})

def elevage_detail(request, id):
    elevage = get_object_or_404(Elevage, id=id)
    individus = elevage.individus.all()
    return render(request, 'game/elevage_detail.html', {'elevage': elevage, 'individus': individus})

def home(request):
    return render(request, 'game/home.html')

def actions(request, elevage_id):
    elevage = get_object_or_404(Elevage, id=elevage_id)
    regle = Regle.objects.first()

    if request.method == 'POST':
        form = Actions(request.POST, elevage=elevage)
        if form.is_valid():
            male_rabbits_to_sell = form.cleaned_data['male_rabbits_to_sell']
            female_rabbits_to_sell = form.cleaned_data['female_rabbits_to_sell']
            food_to_buy = form.cleaned_data['food_to_buy']
            cages_to_buy = form.cleaned_data['cages_to_buy']

            if male_rabbits_to_sell > 0:
                male_rabbits = elevage.individus.filter(sex='M', state='present')[:male_rabbits_to_sell]
                for rabbit in male_rabbits:
                    rabbit.state = 'sold'
                    rabbit.save()

            if female_rabbits_to_sell > 0:
                female_rabbits = elevage.individus.filter(sex='F', state='present')[:female_rabbits_to_sell]
                for rabbit in female_rabbits:
                    rabbit.state = 'sold'
                    rabbit.save()

            elevage.male_rabbits -= male_rabbits_to_sell
            elevage.female_rabbits -= female_rabbits_to_sell
            elevage.money += (male_rabbits_to_sell + female_rabbits_to_sell) * regle.rabbit_sale_price
            elevage.foodLevel += food_to_buy
            elevage.cageNumber += cages_to_buy
            elevage.money -= (food_to_buy * regle.food_price + cages_to_buy * regle.cage_price)
            
            
            update_food_and_advance_month(elevage)
            elevage.save()
            return redirect('elevage_detail', id=elevage.id)
    else:
        form = Actions(elevage=elevage)
    return render(request, 'game/actions.html', {'form': form, 'elevage': elevage})

