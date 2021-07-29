from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from django import forms

from job_search.models import Company


class CompanyCreateForm(forms.ModelForm):

    class Meta:
        model = Company
        field = ['__all__']
        exclude = ('owner',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.label_class = 'mb-2 text-dark'
        self.helper.field_class = 'form-group pb-2'


