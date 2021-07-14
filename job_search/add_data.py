import datetime

from .models import Company, Speciality, Vacancy
from data import companies, specialties, jobs


def add_companies(companies: list):
    for company in companies:
        Company.objects.create(
            id=int(company['id']),
            title=company['title'],
            logo=company['logo'],
            employee_count=company['employee_count']
        )


def add_specialities(specialities: list):
    for speciality in specialities:
        Speciality.objects.create(
            code=speciality['code'],
            title=speciality['title']
        )


def add_jobs(jobs: list):
    for job in jobs:
        Vacancy.objects.create(
            id=int(job['id']),
            title=job['title'],
            specialty=job['specialty'],
            company_id=int(job['company']),
            salary_min=int(job['salary_from']),
            salary_max=int(job['salaty_to']),
            published_at=datetime.date(job['posted']),
            skills=job['skills'],
            description=job['description']
        )
