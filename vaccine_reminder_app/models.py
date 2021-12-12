from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class VaccineName(models.Model):
    name = models.CharField(max_length=55, )
    description = RichTextField(null=True, blank=True, )

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


    