from django.db import models
from ckeditor.fields import RichTextField
from datetime import timedelta

from rest_framework.fields import ReadOnlyField

# Create your models here.

class VaccineName(models.Model):
    name = models.CharField(max_length=55, )
    description = RichTextField(null=True, blank=True, )
    first_dose_age = models.PositiveIntegerField(null=True, blank=True, )
    second_dose_age = models.PositiveIntegerField(null=True, blank=True, )
    third_dose_age = models.PositiveIntegerField(null=True, blank=True, )
    fourth_dose_age = models.PositiveIntegerField(null=True, blank=True, )


    def __str__(self):
        return self.name



class Vaccination(models.Model):
    vaccination_details = RichTextField()


class VaccineReminderRegistration(models.Model):
    
    name = models.CharField(max_length=55, )
    father_name = models.CharField(max_length=55, )
    mother_name = models.CharField(max_length=55, )
    date_of_birth = models.DateField(null=True, )
    gender = models.CharField(max_length=15, )
    email = models.EmailField(null=True, )
    phone = models.CharField(max_length=15, )
    address = models.CharField(max_length=263, )

    def __str__(self):
        return self.name


class VaccineSchedule(models.Model):
    vaccine_name = models.ForeignKey(VaccineName, on_delete=models.CASCADE, null=True, blank=True, related_name='vaccine_name')
    vaccine_user = models.ForeignKey(VaccineReminderRegistration, on_delete=models.CASCADE, )
    first_dose_completed = models.BooleanField(default=False, )
    second_dose_completed = models.BooleanField(default=False, )
    third_dose_completed = models.BooleanField(default=False, )
    fourth_dose_completed = models.BooleanField(default=False, )
    first_dose_vaccine_date = models.DateField(null=True, blank=True, )
    second_dose_vaccine_date = models.DateField(null=True, blank=True, )
    third_dose_vaccine_date = models.DateField(null=True, blank=True, )
    fourth_dose_vaccine_date = models.DateField(null=True, blank=True, )


    @property
    def completed(self):
        if (self.first_dose_completed == True) and (self.second_dose_completed==True) and (self.third_dose_completed ==True, ) and (self.fourth_dose_completed==True):
            return True
        else:
            return False 

    @property
    def first_dose_date(self):
        dob = self.vaccine_user.date_of_birth
        delta = timedelta(days=self.vaccine_name.first_dose_age)
        vaccine_date = dob + delta
        return vaccine_date
        # self.first_dose_vaccine_date = vaccine_date.strftime('%m/%d/%Y')

    @property
    def second_dose_date(self):
        dob = self.vaccine_user.date_of_birth
        delta = timedelta(days=self.vaccine_name.second_dose_age)
        vaccine_date = dob + delta
        return vaccine_date
        # self.second_dose_vaccine_date = vaccine_date

    @property
    def third_dose_date(self):
        dob = self.vaccine_user.date_of_birth
        delta = timedelta(days=self.vaccine_name.third_dose_age)
        vaccine_date = dob + delta
        return vaccine_date
        # self.third_dose_vaccine_date = vaccine_date.strftime('%m/%d/%Y')
    
    @property
    def fourth_dose_date(self):
        dob = self.vaccine_user.date_of_birth
        delta = timedelta(days=self.vaccine_name.fourth_dose_age)
        vaccine_date = dob + delta
        return vaccine_date

    def save(self, *args, **kwargs):
        self.first_dose_vaccine_date = self.first_dose_date
        self.second_dose_vaccine_date = self.second_dose_date
        self.third_dose_vaccine_date = self.third_dose_date
        self.fourth_dose_vaccine_date = self.fourth_dose_date
        super(VaccineSchedule, self).save(*args, **kwargs)    
    
    def __str__(self):
        return f'{ self.vaccine_name.name} vaccine schedule for {self.vaccine_user.name}'



    