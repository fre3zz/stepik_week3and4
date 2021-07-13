from django.contrib import admin
from django.urls import path, include
from .views import VacancyView

urlpatterns = [
    path('vacancy/', VacancyView.as_view(), name='vacancy')
]