from django.urls import path

from .views import VacancyView, MainView, VacanciesView, CompanyView, VacanciesByCategoryView, CompanyCreateView, \
    CompanyLetsstart, CompanyEditView

urlpatterns = [
    path('vacancies/cat/<str:category>/', VacanciesByCategoryView.as_view(), name='vacancies_by_cat'),
    path('vacancies/<int:vacancy_pk>/', VacancyView.as_view(), name='vacancy'),
    path('', MainView.as_view(), name='index'),
    path('companies/<int:company_pk>/', CompanyView.as_view(), name='company'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('mycompany/', CompanyEditView.as_view(), name='my_company'),
    path('mycompany/letsstart/', CompanyLetsstart.as_view(), name='new_company'),
    path('mycompany/create', CompanyCreateView.as_view(), name='create_company'),
    path()


]
