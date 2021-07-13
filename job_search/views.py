from django.shortcuts import render
# Create your views here.
from django.views.generic import TemplateView


class VacancyView(TemplateView):
    template_name = 'job_search/vacancy.html'

