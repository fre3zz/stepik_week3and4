from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.views.generic import TemplateView, ListView

from .models import Vacancy


class VacancyView(TemplateView):
    template_name = 'job_search/vacancy.html'
    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        context['vacancy'] = get_object_or_404(Vacancy, pk=context['pk'])
        print(context)
        return context



class MainView(TemplateView):
    template_name = 'job_search/index.html'


class VacanciesView(TemplateView):
    template_name = 'job_search/vacancies.html'


class CompanyView(TemplateView):
    template_name = 'job_search/company.html'
