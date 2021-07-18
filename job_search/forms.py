from django.forms import ModelForm

from job_search.models import Company


class CompanyCreateForm(ModelForm):
    class Meta:
        model = Company
        exclude = ('owner',)


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('owner')
        super().__init__(*args, **kwargs)