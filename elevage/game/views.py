from django.shortcuts import render, redirect, get_object_or_404
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

def elevage_detail(request, id):
    elevage = get_object_or_404(Elevage, id=id)
    return render(request, 'game/elevage_detail.html', {'elevage': elevage})

def home(request):
    return render(request, 'game/home.html')