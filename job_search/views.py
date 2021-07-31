from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404, HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView

from .forms import CompanyCreateForm
from .models import Vacancy, Company, Speciality


class VacancyView(TemplateView):
    template_name = 'job_search/vacancy.html'

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        context['vacancy'] = get_object_or_404(Vacancy, pk=context['vacancy_pk'])  # объект по ключу из url
        return context


class MainView(TemplateView):
    template_name = 'job_search/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['companies'] = Company.objects.annotate(num_vacancies=Count('vacancies'))
        context['specialities'] = Speciality.objects.annotate(num_vacancies=Count('vacancies'))
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
        return context


class CompanyLetsstart(LoginRequiredMixin, TemplateView):
    template_name = 'job_search/company_create.html'


class CompanyCreateView(LoginRequiredMixin, View):

    def get(self, request):
        company_form = CompanyCreateForm()
        context = {
            'form': company_form,
        }
        return render(request, template_name='job_search/company_new.html', context=context)

    def post(self, request):

        company_form = CompanyCreateForm(request.POST, request.FILES)

        if company_form.is_valid():
            new_company = company_form.save(commit=False)
            new_company.owner = request.user
            new_company.save()

        return HttpResponseRedirect(reverse('my_company'))


class CompanyEditView(LoginRequiredMixin, View):
    # Вью для просмотра и редактирования информации о компании
    # При переходе на 'my_company' проверяет привязана ли компания к пользователю.
    # Если компании нет, то кидает на 'new_company'
    # Если есть, то на страницу редактирования компании
    # я не сообразил как заставить по дефолту указывать существующий url картинки,
    # поэтому проверка на дефолтный урл logo_default_url
    logo_default_url = '/media/https%3A/place-hold.it/100x60'
    def get(self, request):
        try:
            company = Company.objects.get(owner=request.user)
        except Company.DoesNotExist:
            return HttpResponseRedirect(reverse('new_company'))
        company_form = CompanyCreateForm(instance=company)
        context = {
            'form': company_form,
            'company': company
        }
        return render(request, template_name='job_search/company_edit.html', context=context)

    def post(self, request):
        actual_company = get_object_or_404(Company, owner=request.user)
        company_form = CompanyCreateForm(request.POST, request.FILES)

        if company_form.is_valid():
            new_company = company_form.save(commit=False)
            print(new_company.logo.url)
            if new_company.name != actual_company.name:
                actual_company.name = new_company.name
            if new_company.logo.url != self.logo_default_url and new_company.logo != actual_company.logo:
                actual_company.logo = new_company.logo
            if new_company.employee_count != actual_company.employee_count:
                actual_company.employee_count = new_company.employee_count
            if new_company.description != actual_company.description:
                actual_company.description = new_company.description
            if new_company.location != actual_company.location:
                actual_company.location = new_company.location
            actual_company.save()

        return HttpResponseRedirect(reverse('my_company'))



def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Простите извините! (Ошибка 404)')


def custom_handler500(request):
    return HttpResponseServerError('Ой, что то сломалось... Простите извините! (Ошибка 500)')


