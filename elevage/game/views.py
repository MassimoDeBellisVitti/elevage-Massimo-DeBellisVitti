from django.shortcuts import render, redirect
from .forms import ElevageForm

def nouveau(request):
    if request.method == 'POST':
        form = ElevageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ElevageForm()
    return render(request, 'game/nouveau.html', {'form': form})