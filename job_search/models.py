from django import conf
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название компании")
    location = models.CharField(max_length=100, verbose_name="Местоположение")
    logo = models.ImageField(upload_to=conf.settings.MEDIA_COMPANY_IMAGE_DIR, default='logo')
    description = models.TextField(verbose_name="Описание")
    employee_count = models.IntegerField(verbose_name="Количество сотрудников")
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='mycompany')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('index')


class Speciality(models.Model):
    code = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=conf.settings.MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField(max_length=100,  verbose_name='Название вакансии')
    skills = models.TextField(verbose_name='Навыки')
    description = models.TextField(verbose_name='Описание')
    salary_min = models.IntegerField(verbose_name='Минимальная ЗП')
    salary_max = models.IntegerField(verbose_name='Максимальная ЗП')
    published_at = models.DateTimeField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    specialty = models.ForeignKey(Speciality,
                                  on_delete=models.CASCADE,
                                  related_name="vacancies",
                                  verbose_name="Специализация"
                                  )

    def __str__(self):
        return self.title


class Application(models.Model):
    written_username = models.CharField(max_length=100, verbose_name="Ваше имя")
    written_phone = models.CharField(max_length=20, verbose_name="Ваш телефон")
    written_cover_letter = models.TextField(verbose_name="Сопроводительное письмо")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return f"Application from {self.user}"
