import datetime

from django.db import models
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'conf.settings'
# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    logo = models.URLField(default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.IntegerField()


class Speciality(models.Model):
    code = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    picture = models.URLField(default='https://place-hold.it/100x60')


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateTimeField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    specialty = models.ForeignKey(Speciality, on_delete=models.CASCADE, related_name="vacancies")
