# Generated by Django 4.0.6 on 2022-08-19 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_actor_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='age',
            field=models.BigIntegerField(verbose_name='Возраст'),
        ),
    ]