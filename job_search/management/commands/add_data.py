import datetime

from django.core.management import BaseCommand

from job_search.models import Company, Speciality, Vacancy
from job_search.data import companies, specialties, jobs


class Command(BaseCommand):
    def handle(self, *args, **options):

        for company in companies:
            Company.objects.create(
                id=int(company['id']),
                name=company['title'],
                logo=company['logo'],
                location=company['location'],
                employee_count=company['employee_count'],
                description=company['description']
            )

        for speciality in specialties:
            Speciality.objects.create(
                code=speciality['code'],
                title=speciality['title']
            )

        for job in jobs:
            Vacancy.objects.create(
                id=int(job['id']),
                title=job['title'],
                specialty=Speciality.objects.get(code=job['specialty']),
                company_id=int(job['company']),
                salary_min=int(job['salary_from']),
                salary_max=int(job['salary_to']),
                published_at=datetime.date.fromisoformat(job['posted'], locale='ru_RU'),
                skills=job['skills'],
                description=job['description']
            )
