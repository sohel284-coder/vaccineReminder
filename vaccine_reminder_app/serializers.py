from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from vaccine_reminder_app.models import VaccineReminderRegistration, VaccineSchedule

class VaccineReminderRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineReminderRegistration
        exclude = ('mother_name', ) 

    def validate_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError('email is invalid')    
        return email





class VaccineScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineSchedule
        exclude = ('first_dose_completed', 'second_dose_completed', 'third_dose_completed', 'fourth_dose_completed', )
