from django.contrib import admin
from django.urls import path, re_path
from .views import VacancyView, MainView, VacanciesView, CompanyView

urlpatterns = [
    path('vacancies/<int:vacancy_pk>/', VacancyView.as_view(), name='vacancy'),
    path('', MainView.as_view(), name='index'),
    path('companies/<int:company_pk>/', CompanyView.as_view(), name='company'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:category>/', VacanciesView.as_view(), name='vacancies_by_cat')
]