from django.shortcuts import render, redirect
from .models import Elevage, MaleRabbit, FemaleRabbit
from .forms import ElevageForm

def nouveau(request):
    if request.method == 'POST':
        form = ElevageForm(request.POST)
        if form.is_valid():
            elevage = form.save()

            for _ in range(elevage.male_rabbits):
                MaleRabbit.objects.create(elevage=elevage, age=1)

            for _ in range(elevage.female_rabbits):
                FemaleRabbit.objects.create(elevage=elevage, age=1, pregnancyTime=0)

            return redirect('/')
    else:
        form = ElevageForm()
    return render(request, 'game/nouveau.html', {'form': form})

def elevage_list(request):
    elevages = Elevage.objects.all()
    return render(request, 'game/elevage_list.html', {'elevages': elevages})

