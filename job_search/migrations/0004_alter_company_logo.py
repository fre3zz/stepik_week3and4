# Generated by Django 3.2.5 on 2021-07-21 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_search', '0003_alter_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(default='https://place-hold.it/100x60', upload_to='company_images'),
        ),
    ]