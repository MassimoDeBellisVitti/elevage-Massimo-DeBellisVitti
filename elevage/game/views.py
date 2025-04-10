from django.shortcuts import render, redirect, get_object_or_404
from .models import Elevage, Individu
from .forms import ElevageForm, Actions

def nouveau(request):
    if request.method == 'POST':
        form = ElevageForm(request.POST)
        if form.is_valid():
            elevage = form.save()

            for _ in range(int(request.POST.get('male_rabbits', 0))):
                Individu.objects.create(elevage=elevage, sex='M', age=1)

            for _ in range(int(request.POST.get('female_rabbits', 0))):
                Individu.objects.create(elevage=elevage, sex='F', age=1)

            return render(request, 'game/actions.html', {'form': form, 'elevage': elevage})
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

    if request.method == 'POST':
        form = Actions(request.POST)
        if form.is_valid():
            form = Actions()
            return render(request, 'game/actions.html', {'form': form, 'elevage': elevage})
    else:
        form = Actions()

    return render(request, 'game/actions.html', {'form': form, 'elevage': elevage})