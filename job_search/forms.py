from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from django import forms

from job_search.models import Company


class CompanyCreateForm(forms.Form):
    #     name = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)
#     logo = models.URLField(default='https://place-hold.it/100x60')
#     description = models.TextField()
#     employee_count = models.IntegerField()
#     owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.label_class = 'mb-2 text-dark'
        self.helper.field_class = 'form-group pb-2'
        self.helper.layout = Layout(
            Fieldset(
                "TITLE",
                'name',
                'logo'
            )
        )

    name = forms.CharField(label="Название компании", max_length=100)
    location = forms.CharField(label='География', max_length=100)
    logo = forms.ImageField(required=False)
    description = forms.CharField(label='Информация о компании')
    employee_count = forms.IntegerField(label='Количество человек в компании')