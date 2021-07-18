from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, FormView, CreateView

from .forms import CompanyCreateForm
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacanciesView, self).get_context_data(**kwargs)
        context['title'] = "Все вакансии"  # Тайтл в темплэйт
        return context


class VacanciesByCategoryView(ListView):
    # вакансии по специализации
    template_name = 'job_search/vacancies.html'
    model = Vacancy
    context_object_name = 'vacancies'

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super(VacanciesByCategoryView, self).get_context_data(**kwargs)
        category = get_object_or_404(Speciality, code=self.kwargs['category'])
        context['title'] = category.title  # Тайтл в темплэйте.
        return context

    def get_queryset(self):
        try:
            category = self.kwargs['category']
            speciality = get_object_or_404(Speciality, code=category)  # наличие специализации из урла в списке
            return Vacancy.objects.filter(specialty=speciality)   # поиск по специализации
        except KeyError:
            raise Http404


class CompanyView(TemplateView):
    template_name = 'job_search/company.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['company'] = get_object_or_404(Company, pk=context['company_pk'])  # объект по ключу из url
        context['companies_count'] = Company.objects.count()  # передается для перехода на следующую вакансию
        return context


class CompanyLetsstart(TemplateView):
    template_name = 'job_search/company_create.html'


class CompanyCreateView(CreateView):
    template_name = 'job_search/company_edit.html'
    model = Company
    form_class = CompanyCreateForm

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CompanyCreateView, self).get_form_kwargs(*args, *kwargs)
        kwargs['owner'] = self.request.user
        print(self.request)
        return kwargs



def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Простите извините! (Ошибка 404)')


def custom_handler500(request):
    return HttpResponseServerError('Ой, что то сломалось... Простите извините! (Ошибка 500)')


