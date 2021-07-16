from django.http import Http404
from django.shortcuts import get_object_or_404
# Create your views here.
from django.views.generic import TemplateView, ListView

from .models import Vacancy, Company, Speciality


class VacancyView(TemplateView):
    template_name = 'job_search/vacancy.html'

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        context['vacancy'] = get_object_or_404(Vacancy, pk=context['vacancy_pk'])  # объект по ключу из url
        context['vacancies_count'] = Vacancy.objects.count()  # передается для перехода на следующую вакансию
        return context


class MainView(TemplateView):
    template_name = 'job_search/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        context['specialities'] = Speciality.objects.all()
        return context


class VacanciesView(ListView):
    template_name = 'job_search/vacancies.html'
    model = Vacancy
    context_object_name = 'vacancies'

    def get_queryset(self):

        if self.kwargs:  # если урл что-то передает
            category = self.kwargs['category']
            if Speciality.objects.filter(code=category).count() > 0:
                return Vacancy.objects.filter(specialty__code=category)   # поиск по свециализации
            else:
                raise Http404
        else:  # вывод всех вакансий
            return Vacancy.objects.all()


class CompanyView(TemplateView):
    template_name = 'job_search/company.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['company'] = get_object_or_404(Company, pk=context['company_pk'])  # объект по ключу из url
        context['companies_count'] = Company.objects.count()  # передается для перехода на следующую вакансию
        return context
