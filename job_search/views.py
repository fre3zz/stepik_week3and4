from django.shortcuts import render
# Create your views here.
from django.views.generic import TemplateView, ListView

from .models import Vacancy


class VacancyView(TemplateView):
    template_name = 'job_search/vacancy.html'
    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        context['vacancy'] = Vacancy.objects.get(id=context['pk'])
        print(context)
        return context



class MainView(TemplateView):
    template_name = 'job_search/index.html'


class VacanciesView(TemplateView):
    template_name = 'job_search/vacancies.html'


class CompanyView(TemplateView):
    template_name = 'job_search/company.html'
