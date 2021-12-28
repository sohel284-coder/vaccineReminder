# Generated by Django 3.2 on 2021-12-18 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine_reminder_app', '0007_auto_20211218_0639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccinename',
            name='first_dose_age',
            field=models.PositiveIntegerField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='vaccinename',
            name='fourth_dose_age',
            field=models.PositiveIntegerField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='vaccinename',
            name='second_dose_age',
            field=models.PositiveIntegerField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='vaccinename',
            name='third_dose_age',
            field=models.PositiveIntegerField(blank=True, max_length=32, null=True),
        ),
    ]
