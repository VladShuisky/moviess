# Generated by Django 4.0.6 on 2022-08-19 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='age',
            field=models.DateField(auto_now=True, verbose_name='Дата рождения'),
        ),
    ]
