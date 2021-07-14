from django.shortcuts import render
# Create your views here.
from django.views.generic import TemplateView, ListView


class VacancyView(TemplateView):
    template_name = 'job_search/vacancy.html'


class MainView(TemplateView):
    template_name = 'job_search/index.html'


class VacanciesView(TemplateView):
    template_name = 'job_search/vacancies.html'


class CompanyView(TemplateView):
    template_name = 'job_search/company.html'
