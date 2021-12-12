from django.db.models import fields
from rest_framework import serializers

from vaccine_reminder_app.models import VaccineReminderRegistration

class VaccineReminderRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineReminderRegistration
        exclude = ('mother_name', )