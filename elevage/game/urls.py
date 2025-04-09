from django.urls import path
from .views import nouveau

urlpatterns = [
    path('nouveau/', nouveau, name='nouveau'),
]