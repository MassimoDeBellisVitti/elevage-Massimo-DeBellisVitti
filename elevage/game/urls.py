from django.urls import path
from .views import nouveau, elevage_list, elevage_detail

urlpatterns = [
    path('elevage_list/', elevage_list, name='elevage_list'),
    path('nouveau/', nouveau, name='nouveau'),
    path('elevage/<int:id>/', elevage_detail, name='elevage_detail'),
]