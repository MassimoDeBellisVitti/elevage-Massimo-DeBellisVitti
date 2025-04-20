from django.shortcuts import render, redirect, get_object_or_404
from .models import Elevage, Individu, Regle
from .forms import ElevageForm, Actions
from .services import process_actions, update, calculate_monthly_food_consumption

def nouveau(request):
    regle = Regle.objects.first()
    initial_budget = regle.budget_limit

    if request.method == 'POST':
        form = ElevageForm(request.POST)
        if form.is_valid():
            elevage = form.save(commit=False)
            male_rabbits = int(request.POST.get('male_rabbits', 0))
            female_rabbits = int(request.POST.get('female_rabbits', 0))
            food = int(request.POST.get('foodLevel', 0))
            cages = int(request.POST.get('cageNumber', 0))

            total_cost = (
                male_rabbits * regle.male_rabbit_price +
                female_rabbits * regle.female_rabbit_price +
                food * regle.food_price +
                cages * regle.cage_price
            )

            if total_cost > initial_budget:
                form.add_error(None, "Not enough money to create this farm.")
            else:
                elevage.money = initial_budget - total_cost
                elevage.foodLevel = food*1000
                elevage.save()

                for _ in range(male_rabbits):
                    Individu.objects.create(elevage=elevage, sex='M', age=1)

                for _ in range(female_rabbits):
                    Individu.objects.create(elevage=elevage, sex='F', age=1)

                return redirect('elevage_detail', id=elevage.id)
    else:
        form = ElevageForm(initial={
            'money': initial_budget,
            'male_rabbits': 0,
            'female_rabbits': 0,
            'foodLevel': 0,
            'cageNumber': 0
        })

    return render(request, 'game/nouveau.html', {
        'form': form,
        'regle': regle,  
        'initial_budget': initial_budget  
    })

def elevage_list(request):
    elevages = Elevage.objects.all()
    return render(request, 'game/elevage_list.html', {'elevages': elevages})

def elevage_detail(request, id):
    elevage = get_object_or_404(Elevage, id=id)
    show_all = request.GET.get('show_all', 'false') == 'true'
    monthly_food_consumption = calculate_monthly_food_consumption(elevage)

    if show_all:
        individus = elevage.individus.all()
    else:
        individus = elevage.individus.exclude(state__in=['dead', 'sold'])

    male_rabbits = individus.filter(sex='M').order_by('-age')
    female_rabbits = individus.filter(sex='F').order_by('-age')

    male_rabbits_by_age = {
        1: male_rabbits.filter(age=1),
        2: male_rabbits.filter(age=2),
        'older': male_rabbits.filter(age__gt=2),
    }

    female_rabbits_by_age = {
        1: female_rabbits.filter(age=1),
        2: female_rabbits.filter(age=2),
        'younger_than_6': female_rabbits.filter(age__gt=2, age__lt=6),
        '6_or_older': female_rabbits.filter(age__gt=5),
    }

    if request.method == 'POST':
        form = Actions(request.POST, elevage=elevage)
        if form.is_valid():
            male_rabbits_to_sell = form.cleaned_data['male_rabbits_to_sell']
            female_rabbits_to_sell = form.cleaned_data['female_rabbits_to_sell']
            food_to_buy = form.cleaned_data['food_to_buy']
            cages_to_buy = form.cleaned_data['cages_to_buy']

            process_actions(elevage, male_rabbits_to_sell, female_rabbits_to_sell, food_to_buy, cages_to_buy)
            update(elevage)

            return redirect('elevage_detail', id=elevage.id)
    else:
        form = Actions(elevage=elevage)

    return render(request, 'game/elevage_detail.html', {
        'elevage': elevage,
        'male_rabbits_by_age': male_rabbits_by_age,
        'female_rabbits_by_age': female_rabbits_by_age,
        'form': form,
        'show_all': show_all,
        'monthly_food_consumption': monthly_food_consumption
    })

def home(request):
    return render(request, 'game/home.html')

def rules(request):
    return render(request, 'game/rules.html')

