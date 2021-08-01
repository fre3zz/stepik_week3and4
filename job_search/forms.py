from django import forms

from job_search.models import Company, Vacancy, Application


class CompanyCreateForm(forms.ModelForm):

    class Meta:
        model = Company
        field = [
            'name',
            'location',
            'logo',
            'description',
            'employee_count'
        ]
        exclude = ('owner',)


class VacancieCreateForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        field = [
            'title',
            'skills',
            'description',
            'salary_min',
            'salary_max',
            'specialty'
        ]
        exclude = ('company', 'published_at')

    def clean(self):
        super(VacancieCreateForm, self).clean()
        salary_min = self.cleaned_data.get('salary_min')
        salary_max = self.cleaned_data.get('salary_max')
        if salary_min > salary_max:
            self.add_error('salary_min', 'Min > Max')


class ApplicationCreateForm(forms.ModelForm):

    class Meta:
        model = Application
        field = [
            'written_username',
            'written_phone',
            'written_cover_letter'
        ]
        exclude = ('vacancy', 'user')
