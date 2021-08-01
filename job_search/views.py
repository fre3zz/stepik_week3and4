from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404, HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView

from .forms import CompanyCreateForm, VacancieCreateForm, ApplicationCreateForm
from .models import Vacancy, Company, Speciality, Application


class VacancyView(TemplateView):
    template_name = 'job_search/vacancy.html'

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        context['vacancy'] = get_object_or_404(Vacancy, pk=context['vacancy_pk'])  # объект по ключу из url
        application_form = ApplicationCreateForm()
        context['form'] = application_form
        return context

    def post(self, request, vacancy_pk):
        application_form = ApplicationCreateForm(request.POST)
        if application_form.is_valid():
            new_application = application_form.save(commit=False)
            new_application.vacancy = get_object_or_404(Vacancy, id=vacancy_pk)
            new_application.user = request.user
            new_application.save()
            return HttpResponseRedirect(reverse('application_send'))


def application_send(request):
    return render(request, template_name='job_search/application_send.html')


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
        return render(request, template_name='job_search/company_edit.html', context=context)

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
    logo_default_url = 'logo'

    def get(self, request):
        try:
            company = Company.objects.get(owner=request.user)
        except Company.DoesNotExist:
            return HttpResponseRedirect(reverse('new_company'))
        company_form = CompanyCreateForm(instance=company)
        context = {
            'form': company_form,
            'company': company  # для отображения логотипа
        }
        return render(request, template_name='job_search/company_edit.html', context=context)

    def post(self, request):
        actual_company = get_object_or_404(Company, owner=request.user)
        company_form = CompanyCreateForm(request.POST, request.FILES)
        edited = False
        if company_form.is_valid():
            for field_name, field_value in company_form.cleaned_data.items():
                # logo обрабатывается по другому, так как не поборол проблему с дефолтным...
                # При обновлении формы через render logo скидывается на дефолтное
                # соответственно, если дефолтное или поменялось, то меняем на новое
                if field_value != getattr(actual_company, field_name) and field_name != 'logo':
                    setattr(actual_company, field_name, field_value)
                    edited = True
                if field_name == 'logo' and field_value not in \
                        [
                            self.logo_default_url,
                            getattr(actual_company, field_name)
                        ]:
                    actual_company.logo.storage.delete(actual_company.logo.path)
                    setattr(actual_company, field_name, field_value)
                    edited = True

            if edited:
                actual_company.save()

            company_form = CompanyCreateForm(instance=actual_company)
            context = {
                'form': company_form,
                'company': actual_company,  # для отображения картинки
                'edited': edited
            }
            return render(request, template_name='job_search/company_edit.html', context=context)


class MyCompanyVacancies(LoginRequiredMixin, View):
    template_name = 'job_search/myvacancies.html'

    def get(self, request):
        try:
            company = Company.objects.get(owner=self.request.user)
        except Company.DoesNotExist:
            return HttpResponseRedirect(reverse('new_company'))

        vacancies = Vacancy.objects.filter(company=company).annotate(num_applications=Count('applications'))

        context = {
            'vacancies': vacancies
        }
        return render(request, template_name=self.template_name, context=context)


class MyCompanyNewVacancy(LoginRequiredMixin, View):
    template = 'job_search/vacancy_edit.html'
    # класс для создания новой вакансии

    def get(self, request):
        vacancy_form = VacancieCreateForm()
        context = {
            'vacancy_form': vacancy_form
        }
        return render(request, template_name=self.template, context=context)

    def post(self, request):
        vacancy_form = VacancieCreateForm(request.POST)

        if vacancy_form.is_valid():
            new_vacancy = vacancy_form.save(commit=False)
            try:
                company = Company.objects.get(owner=request.user)
            except Company.DoesNotExist:
                return HttpResponseRedirect(reverse('new_company'))
            new_vacancy.company = company
            new_vacancy.published_at = datetime.today()
            new_vacancy.save()

        return HttpResponseRedirect(reverse('my_vacancies'))


class MyCompanyEditVacancy(LoginRequiredMixin, View):
    template = 'job_search/vacancy_edit.html'

    def get(self, request, vacancy_pk):
        try:
            company = Company.objects.get(owner=request.user)
        except Company.DoesNotExist:
            return redirect('new_company')

        try:
            vacancy = Vacancy.objects.get(id=vacancy_pk, company=company)
        except Vacancy.DoesNotExist:
            return redirect('my_vacancies')

        vacancy_form = VacancieCreateForm(instance=vacancy)
        applications = Application.objects.filter(vacancy=vacancy)
        context = {
            'vacancy_form': vacancy_form,
            'applications': applications
        }
        return render(request, template_name=self.template, context=context)

    def post(self, request, vacancy_pk):
        vacancy_form = VacancieCreateForm(request.POST)
        try:
            company = Company.objects.get(owner=request.user)
        except Company.DoesNotExist:
            return redirect('new_company')

        try:
            actual_vacancy = Vacancy.objects.get(id=vacancy_pk, company=company)
        except Vacancy.DoesNotExist:
            return redirect('my_vacancies')
        edited = False
        if vacancy_form.is_valid():
            # Проверка на то, что нужно поменять в актуальной вакансии
            # Если ничего не поменялось, то просто редирект, если менялось, то добавляется edited = True
            for field_name, field_value in vacancy_form.cleaned_data.items():
                if field_value != getattr(actual_vacancy, field_name):
                    setattr(actual_vacancy, field_name, field_value)
                    edited = True
            if edited:
                actual_vacancy.published_at = datetime.today()
                actual_vacancy.save()
        context = {
            'vacancy_form': vacancy_form,
            'edited': edited
        }
        return render(request, template_name=self.template, context=context)


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Простите извините! (Ошибка 404)')


def custom_handler500(request):
    return HttpResponseServerError('Ой, что то сломалось... Простите извините! (Ошибка 500)')
