from django.contrib import admin

from vaccine_reminder_app.models import Vaccination, VaccineName, VaccineReminderRegistration


admin.site.register(VaccineReminderRegistration)
admin.site.register(Vaccination)
admin.site.register(VaccineName)
