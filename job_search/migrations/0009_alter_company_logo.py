# Generated by Django 3.2.5 on 2021-07-31 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_search', '0008_alter_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(default='logo', upload_to='company_images'),
        ),
    ]