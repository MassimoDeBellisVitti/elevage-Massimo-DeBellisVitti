from django.shortcuts import render, redirect, get_object_or_404
from .models import Elevage, Individu, Regle
from .forms import ElevageForm, Actions
from .services import process_actions, update

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
    show_all = request.GET.get('show_all', 'false') == 'true'

    if show_all:
        individus = elevage.individus.all()
    else:
        individus = elevage.individus.exclude(state__in=['dead', 'sold'])

    male_rabbits = individus.filter(sex='M').order_by('-age')
    female_rabbits = individus.filter(sex='F').order_by('-age')

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
        'male_rabbits': male_rabbits,
        'female_rabbits': female_rabbits,
        'form': form,
        'show_all': show_all
    })

def home(request):
    return render(request, 'game/home.html')

